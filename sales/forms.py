from django import forms
from .models import Quotation, SalesOrder, SalesItem

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['client', 'quotation_number', 'valid_until', 'status', 'notes']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'quotation_number': forms.TextInput(attrs={'class': 'form-control'}),
            'valid_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ['client', 'order_number', 'status']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class SalesItemForm(forms.ModelForm):
    class Meta:
        model = SalesItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
