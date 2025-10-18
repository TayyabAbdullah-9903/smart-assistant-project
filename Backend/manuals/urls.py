# manuals/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_manual, name='upload_manual'),
]