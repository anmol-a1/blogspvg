"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from .import views
from django import urls
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name="home"),
    path('contact/',views.contact,name="contact"),
    path('about/',views.about,name="about"),
    path('myblogs/',views.myblogs,name="myblogs"),
    path('trending/',views.trending,name="trending"),
    path('loginsignup/',views.loginsignup,name="loginsignup"),
    path('login/',views.logindof,name="login"),
    path('signup/',views.signupdof,name="signup"),
    path('logout/',views.logoutdof,name="logout"),
    path('blog/postcomment/',views.postcomment,name="postcomment"),
    path('blog/<str:title>',views.blog,name="blog"),
    path('bloglikes/<str:title>',views.bloglikes,name="bloglikes"),
    path('search/',views.search,name="search"),
    path('saveblogpost/',views.saveblogpost,name='saveblogpost'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('changepassword/<token>',views.changepassword,name='changepassword')
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
