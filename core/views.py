from django.shortcuts import render

def home(request):
    """
    Main dashboard view.
    """
    context = {
        'total_clients': 0, # Placeholder
        'total_providers': 0,
        'active_orders': 0,
        'monthly_sales': 0
    }
    return render(request, 'core/dashboard.html', context)
