from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import PurchaseOrder, Product, PurchaseOrderItem
from .forms import PurchaseOrderForm, ProductForm, PurchaseOrderItemForm

# Product Catalog Views
def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'purchases/product_list.html', {'page_obj': page_obj})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'purchases/product_form.html', {'form': form, 'title': 'Nuevo Producto'})

# Order Views
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
import json

# Order Views
def order_dashboard(request):
    # Date Filter
    date_range = request.GET.get('range', 'month')
    now = timezone.now()
    if date_range == 'week':
        start_date = now - timedelta(days=7)
    elif date_range == 'today':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    else: # month
        start_date = now - timedelta(days=30)

    # Base Queryset
    orders = PurchaseOrder.objects.filter(created_at__gte=start_date).order_by('-date_issued')

    # Stats
    total_orders = orders.count()
    completed_orders = orders.filter(status='received').count()
    total_spent = orders.exclude(status='cancelled').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_orders = orders.filter(status__in=['sent', 'approved']).count()

    # Chart Data (Spending Trend)
    spending_by_day = orders.exclude(status='cancelled').annotate(day=TruncDay('created_at')).values('day').annotate(total=Sum('total_amount')).order_by('day')
    
    chart_labels = []
    chart_data = []
    
    for item in spending_by_day:
        if item['day']:
            chart_labels.append(item['day'].strftime('%Y-%m-%d'))
            chart_data.append(float(item['total']))

    context = {
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'total_spent': total_spent,
        'pending_orders': pending_orders,
        'date_range': date_range,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'purchases/order_dashboard.html', context)

def order_list(request):
    orders = PurchaseOrder.objects.all().order_by('-date_issued')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'purchases/order_list.html', {'page_obj': page_obj})

def order_create(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = PurchaseOrderForm()
    return render(request, 'purchases/order_form.html', {'form': form, 'title': 'Nueva Orden de Compra'})

def order_detail(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    items = order.items.all()
    
    # Handle item addition
    if request.method == 'POST':
        item_form = PurchaseOrderItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.purchase_order = order
            item.save()
            # Update total
            order.total_amount = sum(i.total_line for i in items) + item.total_line
            order.save()
            return redirect('order_detail', pk=pk)
    else:
        item_form = PurchaseOrderItemForm()

    return render(request, 'purchases/order_detail.html', {'order': order, 'items': items, 'item_form': item_form})
