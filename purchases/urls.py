from django.urls import path
from . import views

urlpatterns = [
    # Catalog
    path('products/', views.product_list, name='product_list'),
    path('products/new/', views.product_create, name='product_create'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/new/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
]
