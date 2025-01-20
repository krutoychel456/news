from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import News
from django.urls import reverse
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

def create_image(filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
        data = BytesIO()
        Image.new(image_mode, size).save(data, image_format)
        data.seek(0)
        return data

User = get_user_model()

# class NewsTest(TestCase):
#     def setUp(self):
#         admin_user = User(username='admin', email='admin@admin.com')
#         admin_user.is_staff = True
#         admin_user.is_superuser = True
#         admin_user.set_password('admin')
#         admin_user.save()
#         self.admin = admin_user
#         self.admin_name = 'admin'
#         self.admin_password = 'admin'
#         registered_user = User(username='registered', email='registered@registered.com')
#         registered_user.is_staff = False
#         registered_user.is_superuser = False
#         registered_user.set_password('registered')
#         registered_user.save()
#         self.registered = registered_user

#         n1 = News.objects.create(
#             author=self.admin,
#             article='news 1 article',
#             body='body 1 article'
#         )

#     def test_setup_user_count(self):
#         user_count = User.objects.count()
#         self.assertEqual(user_count, 2)

#     def test_all_access_view(self):
#         self.client.login(username=self.admin_name, password=self.admin_password)
#         response = self.client.get(reverse('detail-news', args=(1,)))
#         self.assertTrue(response.status_code == 200)

#     def test_forbidden_regular_access_view(self):
#         self.client.login(username='registered', password='registered')
#         response = self.client.post('/news/create/', {'article': 'denied'})
#         self.assertEqual(response.status_code, 403)
    
#     def test_allowed_admin_access_view(self):
#         self.client.login(username='admin', password='admin')
#         response = self.client.post('/news/create/', {'article': 'allowed'} )
#         self.assertTrue(response.status_code == 302)
#         created_news = News.objects.filter(article='allowed')
#         self.assertEqual(len(created_news), 1)

#     def test_valid_image_upload(self):
#         url = '/news/create/'
#         temp_image = create_image('test_temp.png')
#         temp_image_file = SimpleUploadedFile('test-temo_image.png', temp_image.getvalue())
#         data = {'article': 'test_image', 'image': temp_image_file}
#         self.client.login(username=self.admin_name, password=self.admin_password)
#         response = self.client.post(url, data, follow=True)
#         self.assertEqual(response.status_code, 200)
#         news_count = News.objects.all().count()
#         self.assertEqual(news_count, 2)

class MySeleniumTests(StaticLiveServerTestCase):
     @classmethod
     def setUpClass(cls):
        super().setUpClass()
        admin_user = User(username='admin', email='admin@admin.com')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password('admin')
        admin_user.save()
        cls.selenium = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.selenium.implicitly_wait(10)
    
     @classmethod
     def tearDownClass(cls):
         cls.selenium.quit()
         super().tearDownClass()

     def test_login(self):
        import time
        self.selenium.get(f'{self.live_server_url}/login/')
        time.sleep(3)
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('admin')
        time.sleep(1)
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('admin')
        time.sleep(1)

        self.selenium.find_element(By.XPATH, '//input[@value="Войти"]').click()
        time.sleep(1)

        nav = self.selenium.find_element(By.TAG_NAME, 'nav')
        nav.screenshot('nav_test_screenshot.png')

        self.assertTrue('admin' in nav.text)
        self.selenium.find_element(By.LINK_TEXT, 'Выйти').click()
        time.sleep(1)