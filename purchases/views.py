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
