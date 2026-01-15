from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Quotation, SalesOrder, SalesItem
from .forms import QuotationForm, SalesOrderForm, SalesItemForm

from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
import json

# Quotation Views
def quotation_dashboard(request):
    # Date Filter
    date_range = request.GET.get('range', 'month')
    now = timezone.now()
    if date_range == 'week':
        start_date = now - timedelta(days=7)
    elif date_range == 'today':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    else: # month
        start_date = now - timedelta(days=30)

    # Base Querysets
    quotations = Quotation.objects.filter(created_at__gte=start_date).order_by('-date_issued')
    sales_orders = SalesOrder.objects.filter(created_at__gte=start_date).exclude(status='cancelled')

    # Stats
    total_quotations = quotations.count()
    approved_quotations = quotations.filter(status='approved').count()
    total_sales = sales_orders.aggregate(Sum('total'))['total__sum'] or 0
    orders_count = sales_orders.count()

    # Chart Data (Sales Trend)
    sales_by_day = sales_orders.annotate(day=TruncDay('created_at')).values('day').annotate(total=Sum('total')).order_by('day')
    
    chart_labels = []
    chart_data = []
    
    for item in sales_by_day:
        if item['day']:
            chart_labels.append(item['day'].strftime('%Y-%m-%d'))
            chart_data.append(float(item['total']))

    context = {
        'total_quotations': total_quotations,
        'approved_quotations': approved_quotations,
        'total_sales': total_sales,
        'orders_count': orders_count,
        'date_range': date_range,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'sales/quotation_dashboard.html', context)

def quotation_list(request):
    query = request.GET.get('q') # Optional if we add search later
    
    # Simple list showing all, or we could add simple search/filter logic here too if needed
    list_qs = Quotation.objects.all().order_by('-date_issued')
    
    paginator = Paginator(list_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sales/quotation_list.html', {'page_obj': page_obj})

def quotation_create(request):
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save()
            return redirect('quotation_detail', pk=quotation.pk)
    else:
        form = QuotationForm()
    return render(request, 'sales/quotation_form.html', {'form': form, 'title': 'Nueva Cotización'})

def quotation_detail(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    items = quotation.items.all()
    
    if request.method == 'POST':
        item_form = SalesItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.quotation = quotation
            item.save()
            # Update total logic here
            return redirect('quotation_detail', pk=pk)
    else:
        item_form = SalesItemForm()
        
    return render(request, 'sales/quotation_detail.html', {'quotation': quotation, 'items': items, 'item_form': item_form})

# Sales Order Views
def sales_list(request):
    orders = SalesOrder.objects.all().order_by('-date_issued')
    return render(request, 'sales/sales_list.html', {'orders': orders})
