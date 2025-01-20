from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()
c = Client()

class ProfileException(Exception):
    pass

class ProfileTest(TestCase):

    def setUp(self):
        self.admin_user_test = User(username='test', email='test@test.com')
        self.admin_user_test.is_staff = True
        self.admin_user_test.is_superuser = True
        self.admin_user_test.set_password('test')
        self.admin_user_test.save()
        self.admin_name = 'test'
        self.admin_password = 'test'
    
    def test_admin_user_exists(self):
        user_exists = User.objects.filter(pk=1).exists()
        self.assertEqual(user_exists, True)
        if user_exists:
            admin_user = User.objects.get(pk=1)
            self.assertEqual(admin_user.is_staff, True)
        else:
            raise ProfileException('Admin user not exists')
    
    def test_user_name(self):
        self.assertNotEqual(self.admin_user_test.username, 'sigmo')

    def test_login_url(self):
        login_url = "/login/"
        self.assertEqual(settings.LOGIN_URL, login_url)

    def test_login_request(self):
        login_url = settings.LOGIN_URL
        user_data = {"username": self.admin_name, "password": self.admin_password}
        responce = c.post(login_url, user_data, follow=True)
        status_code = responce.status_code
        redirect_path = responce.request.get("PATH_INFO")
        self.assertEqual(redirect_path, settings.LOGIN_REDIRECT_URL)
        self.assertEqual(status_code, 200)

    def test_user_email(self):
        self.assertNotEqual(self.admin_user_test.email, 'sigmo@sigmo.sigmo')

    def test_admin_is_superuser(self):
        self.assertEqual(self.admin_user_test.is_superuser, True)