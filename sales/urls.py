from django.urls import path
from . import views

urlpatterns = [
    # Quotations
    path('quotations/', views.quotation_list, name='quotation_list'),
    path('quotations/dashboard/', views.quotation_dashboard, name='quotation_dashboard'), # New
    path('quotations/new/', views.quotation_create, name='quotation_create'),
    path('quotations/<int:pk>/', views.quotation_detail, name='quotation_detail'),
    
    # Orders
    path('orders/', views.sales_list, name='sales_list'),
]
