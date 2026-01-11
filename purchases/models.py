from django.db import models
from providers.models import Provider

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    sku = models.CharField(max_length=50, verbose_name="SKU / Código", unique=True)
    description = models.TextField(verbose_name="Descripción", blank=True)
    unit_measure = models.CharField(max_length=20, verbose_name="Unidad de Medida", default="Unidad")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Catálogo de Productos"
    
    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('sent', 'Enviada'),
        ('approved', 'Aprobada'),
        ('received', 'Recibida'),
        ('cancelled', 'Cancelada'),
    ]

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name="Proveedor", related_name="purchases")
    order_number = models.CharField(max_length=50, verbose_name="No. Orden", unique=True)
    date_issued = models.DateField(verbose_name="Fecha de Emisión")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Estatus")
    
    # Financials
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Monto Total")
    currency = models.CharField(max_length=10, default='MXN', verbose_name="Moneda")
    
    notes = models.TextField(verbose_name="Notas", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Orden de Compra"
        verbose_name_plural = "Órdenes de Compra"

    def __str__(self):
        return f"{self.order_number} - {self.provider.name}"

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Unitario")
    
    @property
    def total_line(self):
        return self.quantity * self.unit_price

class PurchaseAttachment(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to='purchases/%Y/%m/', verbose_name="Archivo")
    description = models.CharField(max_length=100, verbose_name="Descripción", blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
