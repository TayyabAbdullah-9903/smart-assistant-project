from django.urls import path
from . import views

urlpatterns = [
    path("", views.portal_home, name="portal_home"),
    path("manual/<int:pk>/", views.manual_detail, name="manual_detail"),
    path("upload/", views.upload_manual, name="upload_manual"),
]
