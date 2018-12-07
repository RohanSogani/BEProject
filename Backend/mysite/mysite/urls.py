"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^appWindow/',include('appWindow.urls')),  #include doesn't require url function
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index),
    url(r'^home/',views.home,name='home'),

    # user auth urls
    url(r'^accounts/login/',views.login_user,name='login'),
    url(r'^accounts/logout/',views.logout_user,name='logout'),
    url(r'^accounts/loggedin/',views.loggedin,name=''),
    url(r'^accounts/invalid/',views.invalid_login,name=''),
    url(r'^register/',views.register,name='register'),
    url(r'^register_success/',views.register_success,name='register_success'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
