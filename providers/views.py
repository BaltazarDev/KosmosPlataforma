from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Provider
from .forms import ProviderForm

def provider_list(request):
    query = request.GET.get('q')
    providers = Provider.objects.all()
    
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
