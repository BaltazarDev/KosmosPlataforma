from django.urls import path
from . import views

urlpatterns = [
    path('', views.logistics_dashboard, name='logistics_dashboard'),
    path('orders/', views.order_list, name='logistics_order_list'),
    path('orders/new/', views.order_create, name='logistics_order_create'),
    path('orders/<int:pk>/', views.order_detail, name='logistics_order_detail'),
    
    # Actions
    path('orders/<int:pk>/add_event/', views.add_event, name='add_logistics_event'),
    path('orders/<int:pk>/upload_doc/', views.upload_document, name='upload_logistics_doc'),
]
