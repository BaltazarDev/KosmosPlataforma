from django.db import models
from clients.models import Client
from purchases.models import Product

class Quotation(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('sent', 'Enviada'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente", related_name="quotations")
    quotation_number = models.CharField(max_length=50, verbose_name="Folio Cotización", unique=True)
    date_issued = models.DateField(auto_now_add=True, verbose_name="Fecha de Emisión")
    valid_until = models.DateField(verbose_name="Válida hasta")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Estatus")
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Total")
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"

    def __str__(self):
        return self.quotation_number

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente de Pago'),
        ('paid', 'Pagada'),
        ('cancelled', 'Cancelada'),
    ]

    quotation = models.OneToOneField(Quotation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cotización Origen")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    order_number = models.CharField(max_length=50, verbose_name="Folio Venta", unique=True)
    date_issued = models.DateField(auto_now_add=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estatus Pago")
    
    # Financials
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Monto Pagado")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Orden de Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return self.order_number
    
    @property
    def balance_due(self):
        return self.total - self.paid_amount

class SalesItem(models.Model):
    # Can be linked to either a quotation or a sales order (usually copied)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Unitario")
    
    @property
    def total_line(self):
        return self.quantity * self.unit_price
