from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import LogisticsOrder, LogisticsEvent, WeightLossRecord
from .forms import LogisticsOrderForm, LogisticsEventForm, WeightLossForm, LogisticsDocumentForm

def logistics_dashboard(request):
    active_orders = LogisticsOrder.objects.filter(status__in=['pending', 'in_transit'])
    ctx = {
        'active_orders': active_orders
    }
    return render(request, 'logistics/dashboard.html', ctx)

def order_list(request):
    orders = LogisticsOrder.objects.all().order_by('-created_at')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'logistics/order_list.html', {'page_obj': page_obj})

def order_create(request):
    if request.method == 'POST':
        form = LogisticsOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('logistics_order_detail', pk=order.pk)
    else:
        form = LogisticsOrderForm()
    return render(request, 'logistics/order_form.html', {'form': form, 'title': 'Nueva Operación Logística'})

def order_detail(request, pk):
    order = get_object_or_404(LogisticsOrder, pk=pk)
    events = order.events.all()
    documents = order.documents.all()
    
    # Handle forms for small additions (events, docs)
    # Kept simple here, would split in real app
    
    return render(request, 'logistics/order_detail.html', {
        'order': order, 
        'events': events,
        'documents': documents
    })

def add_event(request, pk):
    order = get_object_or_404(LogisticsOrder, pk=pk)
    if request.method == 'POST':
        form = LogisticsEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.order = order
            event.save()
            # Auto-update status based on event title? (logic to be added)
    return redirect('logistics_order_detail', pk=pk)

def upload_document(request, pk):
    order = get_object_or_404(LogisticsOrder, pk=pk)
    if request.method == 'POST':
        form = LogisticsDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.order = order
            doc.save()
    return redirect('logistics_order_detail', pk=pk)
