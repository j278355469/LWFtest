"""
URL configuration for LWF project.

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
from django.urls import include, path
from . import views
from django.conf import settings
from django.urls import re_path as url
import django.contrib.auth.views as auth_view
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf import settings

urlpatterns = [
    path('', views.ex_index, name = 'ex_index'), #首頁

    path('search/', views.search, name="search"), #搜尋

    

]
# urlpatterns += staticfiles_urlpatterns()