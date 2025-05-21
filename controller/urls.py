from django.urls import path
from controller import views

urlpatterns = [
    path('', views.control_view, name='control'),
]
