from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import acc


app_name = 'register'

urlpatterns = [
    path('', login_required(acc), name='acc')
]
