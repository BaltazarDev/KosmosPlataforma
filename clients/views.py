from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from .models import Client
from .forms import ClientForm
from django.core.paginator import Paginator
import json

def client_dashboard(request):
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
    total_clients = Client.objects.all().count()
    new_clients = Client.objects.filter(created_at__gte=start_date)
    new_clients_count = new_clients.count()
    
    # Chart Data (New Clients Trend)
    clients_by_day = new_clients.annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id')).order_by('day')
    
    chart_labels = []
    chart_data = []
    
    for item in clients_by_day:
        if item['day']:
            chart_labels.append(item['day'].strftime('%Y-%m-%d'))
            chart_data.append(item['count'])

    context = {
        'total_clients': total_clients,
        'new_clients_count': new_clients_count,
        'date_range': date_range,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'clients/client_dashboard.html', context)

def client_list(request):
    query = request.GET.get('q')
    clients = Client.objects.all().order_by('-created_at')
    
    if query:
        clients = clients.filter(name__icontains=query)
    
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'clients/client_list.html', {'page_obj': page_obj, 'query': query})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'clients/client_form.html', {'form': form, 'title': 'Nuevo Cliente'})

def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/client_form.html', {'form': form, 'title': 'Editar Cliente'})

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'clients/client_detail.html', {'client': client})
