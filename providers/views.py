from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from .models import Provider
from .forms import ProviderForm
import json

def provider_dashboard(request):
    # Date Filter
    date_range = request.GET.get('range', 'month')
    now = timezone.now()
    if date_range == 'week':
        start_date = now - timedelta(days=7)
    elif date_range == 'today':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    else: # month
        start_date = now - timedelta(days=30)

    # Stats
    total_providers = Provider.objects.all().count()
    new_providers = Provider.objects.filter(created_at__gte=start_date)
    new_providers_count = new_providers.count()

    # Chart Data
    providers_by_day = new_providers.annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id')).order_by('day')
    
    chart_labels = []
    chart_data = []
    for item in providers_by_day:
        if item['day']:
            chart_labels.append(item['day'].strftime('%Y-%m-%d'))
            chart_data.append(item['count'])

    context = {
        'total_providers': total_providers,
        'new_providers_count': new_providers_count,
        'date_range': date_range,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'providers/provider_dashboard.html', context)

def provider_list(request):
    query = request.GET.get('q')
    providers = Provider.objects.all().order_by('-created_at')
    
    if query:
        providers = providers.filter(name__icontains=query)
    
    paginator = Paginator(providers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'providers/provider_list.html', {'page_obj': page_obj, 'query': query})

def provider_create(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('provider_list')
    else:
        form = ProviderForm()
    return render(request, 'providers/provider_form.html', {'form': form, 'title': 'Nuevo Proveedor'})

def provider_update(request, pk):
    provider = get_object_or_404(Provider, pk=pk)
    if request.method == 'POST':
        form = ProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('provider_list')
    else:
        form = ProviderForm(instance=provider)
    return render(request, 'providers/provider_form.html', {'form': form, 'title': 'Editar Proveedor'})

def provider_detail(request, pk):
    provider = get_object_or_404(Provider, pk=pk)
    return render(request, 'providers/provider_detail.html', {'provider': provider})
