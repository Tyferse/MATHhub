"""
URL configuration for mathhub project.

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
from django.urls import path, include

from .views import user_login_register


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_login_register, name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('acc/', include('register.urls')),
    path('survey/', include('survey.urls'))
]
