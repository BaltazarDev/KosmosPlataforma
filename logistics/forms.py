from django import forms
from .models import LogisticsOrder, LogisticsEvent, WeightLossRecord, LogisticsDocument

class LogisticsOrderForm(forms.ModelForm):
    class Meta:
        model = LogisticsOrder
        fields = [
            'purchase_order', 'client', 'responsible', 'shipment_id', 
            'booking_number', 'container_number', 'transport_type',
            'origin', 'destination', 'etd', 'eta', 'incoterm',
            'weight_sent', 'status'
        ]
        widgets = {
            'purchase_order': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'responsible': forms.Select(attrs={'class': 'form-control'}),
            'shipment_id': forms.TextInput(attrs={'class': 'form-control'}),
            'booking_number': forms.TextInput(attrs={'class': 'form-control'}),
            'container_number': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_type': forms.Select(attrs={'class': 'form-control'}),
            'origin': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'etd': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'eta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'incoterm': forms.TextInput(attrs={'class': 'form-control'}),
            'weight_sent': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class LogisticsEventForm(forms.ModelForm):
    class Meta:
        model = LogisticsEvent
        fields = ['title', 'description', 'date', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class WeightLossForm(forms.ModelForm):
    class Meta:
        model = WeightLossRecord
        fields = ['lost_quantity', 'reason', 'description']
        widgets = {
            'lost_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class LogisticsDocumentForm(forms.ModelForm):
    class Meta:
        model = LogisticsDocument
        fields = ['file', 'doc_type', 'description']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'doc_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
