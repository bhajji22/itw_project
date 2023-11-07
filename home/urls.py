"""
URL configuration for data_distro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('',views.index,name="home_page"),
    path('about/',views.about,name="about"),
    path('register/',views.register,name="register"),
    path('handlesignup/',views.signup,name="signup"),
    path('signhandler/',views.logging,name="login"),
    path('data_manager/',views.manage,name="manage"),
    path('logout/',views.handlelogout,name="logout"),
    path('protected_file/<int:file_id>/', views.protected_media, name='protected_media'),
    path('downloader/',views.downloader,name="downloader"),
    path('downloader1/',views.downloader1,name="downloader1"),
    path('downloader2/',views.downloader2,name="downloader2"),
    path('downloader3/',views.downloader3,name="downloader3"),
    path('permissions/',views.permissions,name="permissions"),
    path('change_permissions/',views.change_permissions,name="change_permissions"),
    path('contact/',views.contact,name="contact"),
    path('delete_files/',views.delete,name="delete_files"),
    path('delete/',views.deleter,name="delete")
]
