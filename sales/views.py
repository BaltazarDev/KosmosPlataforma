from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Quotation, SalesOrder, SalesItem
from .forms import QuotationForm, SalesOrderForm, SalesItemForm

# Quotation Views
def quotation_list(request):
    quotations = Quotation.objects.all().order_by('-date_issued')
    paginator = Paginator(quotations, 10)
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
