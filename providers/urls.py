from django.urls import path
from . import views

urlpatterns = [
    path('', views.provider_list, name='provider_list'),
    path('new/', views.provider_create, name='provider_create'),
    path('<int:pk>/', views.provider_detail, name='provider_detail'),
    path('<int:pk>/edit/', views.provider_update, name='provider_update'),
]
