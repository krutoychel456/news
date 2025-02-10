from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from news.views import index, detail_view, about, anekdot, test_view, create_view, art, edit_view, delete_view, commentary_view, likes_view, commentary_edit_view, commentary_delete_view, contact
from profiles.views import (
    logout_view, 
    login_view,
    register_view,
    detail_user_view
)                            


urlpatterns = [
    path('', index,name="index"),
    path('logout/', logout_view),
    path('login/', login_view),
    path('register/', register_view),
    path('news/<int:pk>/', detail_view, name='detail-news'),
    path('about/', about),
    path('anekdot/', anekdot),
    path('test_view', test_view),
    path('news/edit/<int:pk>/', edit_view),
    path('news/delete/<int:pk>/', delete_view),
    path('news/create/', create_view),
    path('art/', art),
    path('admin/', admin.site.urls),
    path('news/commentary/<int:pk>/', commentary_view),
    path('news/commentary/edit/<int:pk>/<int:pk2>/', commentary_edit_view),
    path('news/commentary/delete/<int:pk>/<int:pk2>/', commentary_delete_view),
    path('news/like/<int:pk>/', likes_view),
    path('profile/<int:pk>', detail_user_view, name='profile'),
    path('contact/', contact),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )