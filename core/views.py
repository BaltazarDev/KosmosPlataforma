from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from datetime import timedelta
import json

from clients.models import Client
from providers.models import Provider
from sales.models import SalesOrder
from purchases.models import PurchaseOrder

def home(request):
    """
    Main dashboard view with statistics.
    """
    date_range = request.GET.get('range', 'month')
    now = timezone.now()
    
    if date_range == 'week':
        start_date = now - timedelta(days=7)
        label_format = '%d/%m'
    elif date_range == 'today':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        label_format = '%H:%M'
    else: # month
        start_date = now - timedelta(days=30)
        label_format = '%d/%m'

    # Global Counts
    total_clients = Client.objects.count()
    total_providers = Provider.objects.count()

    # Sales Stats (excluding cancelled)
    sales_qs = SalesOrder.objects.filter(date_issued__gte=start_date).exclude(status='cancelled')
    period_sales = sales_qs.aggregate(Sum('total'))['total__sum'] or 0
    active_orders = sales_qs.filter(status='pending').count()

    # Purchases Stats (excluding cancelled and draft)
    purchases_qs = PurchaseOrder.objects.filter(date_issued__gte=start_date).exclude(status__in=['cancelled', 'draft'])
    period_purchases = purchases_qs.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Chart Data Preparation
    # We will aggregate by day for the chart
    sales_by_day = sales_qs.annotate(day=TruncDay('created_at')).values('day').annotate(total=Sum('total')).order_by('day')
    purchases_by_day = purchases_qs.annotate(day=TruncDay('created_at')).values('day').annotate(total=Sum('total_amount')).order_by('day')

    # Create a unified list of dates
    dates = set()
    sales_dict = {}
    purchases_dict = {}

    for item in sales_by_day:
        if item['day']:
            sales_dict[item['day'].strftime('%Y-%m-%d')] = float(item['total'])
            dates.add(item['day'].strftime('%Y-%m-%d'))
            
    for item in purchases_by_day:
        if item['day']:
            purchases_dict[item['day'].strftime('%Y-%m-%d')] = float(item['total'])
            dates.add(item['day'].strftime('%Y-%m-%d'))
    
    sorted_dates = sorted(list(dates))
    
    chart_labels = sorted_dates
    chart_sales = [sales_dict.get(d, 0) for d in sorted_dates]
    chart_purchases = [purchases_dict.get(d, 0) for d in sorted_dates]

    context = {
        'total_clients': total_clients,
        'total_providers': total_providers,
        'active_orders': active_orders,
        'period_sales': period_sales,
        'period_purchases': period_purchases,
        'date_range': date_range,
        'chart_labels': json.dumps(chart_labels),
        'chart_sales': json.dumps(chart_sales),
        'chart_purchases': json.dumps(chart_purchases),
    }
    return render(request, 'core/dashboard.html', context)
