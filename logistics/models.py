from django.db import models
from django.conf import settings
from purchases.models import PurchaseOrder
from clients.models import Client

class LogisticsOrder(models.Model):
    TRANSPORT_TYPES = [
        ('terrestrial', 'Terrestre'),
        ('maritime', 'Marítimo'),
        ('mixed', 'Mixto'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_transit', 'En Tránsito'),
        ('delivered', 'Entregado'),
        ('facturated', 'Facturado'),
        ('closed', 'Cerrado'),
        ('incident', 'Con Incidencia'),
    ]

    # Links
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Orden de Compra (Origen)", related_name="logistics_orders")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente Asociado")
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Responsable Logístico")

    # Key Info
    shipment_id = models.CharField(max_length=50, verbose_name="Shipment ID", unique=True)
    booking_number = models.CharField(max_length=50, verbose_name="Booking / BL", blank=True)
    container_number = models.CharField(max_length=50, verbose_name="No. Contenedor/Caja", blank=True)
    
    transport_type = models.CharField(max_length=20, choices=TRANSPORT_TYPES, verbose_name="Tipo de Transporte")
    
    origin = models.CharField(max_length=100, verbose_name="Origen / Puerto Salida")
    destination = models.CharField(max_length=100, verbose_name="Destino / Puerto Llegada")
    
    etd = models.DateField(verbose_name="Fecha Est. Salida (ETD)", null=True, blank=True)
    eta = models.DateField(verbose_name="Fecha Est. Llegada (ETA)", null=True, blank=True)
    real_arrival_date = models.DateField(verbose_name="Fecha Real Llegada", null=True, blank=True)
    
    incoterm = models.CharField(max_length=10, blank=True, verbose_name="Incoterm")
    
    # Weight Control
    weight_sent = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Peso Enviado (KG)")
    weight_received = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Peso Recibido (KG)")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estatus Operativo")
    
    # Flags
    is_invoiced = models.BooleanField(default=False, verbose_name="Facturado")
    invoice_date = models.DateField(null=True, blank=True, verbose_name="Fecha Facturación")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Orden Logística"
        verbose_name_plural = "Órdenes Logísticas"

    def __str__(self):
        return self.shipment_id

    @property
    def loss_kg(self):
        return self.weight_sent - self.weight_received
    
    @property
    def loss_percentage(self):
        if self.weight_sent > 0:
            return (self.loss_kg / self.weight_sent) * 100
        return 0

class LogisticsEvent(models.Model):
    order = models.ForeignKey(LogisticsOrder, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=100, verbose_name="Evento")
    description = models.TextField(blank=True)
    date = models.DateTimeField(verbose_name="Fecha y Hora")
    location = models.CharField(max_length=100, blank=True, verbose_name="Ubicación")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

class WeightLossRecord(models.Model):
    order = models.ForeignKey(LogisticsOrder, on_delete=models.CASCADE, related_name="loss_records")
    lost_quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Cantidad Perdida (KG)")
    reason = models.CharField(max_length=100, verbose_name="Motivo (Daño, Humedad, etc.)")
    description = models.TextField(blank=True)
    
    recorded_at = models.DateTimeField(auto_now_add=True)

class LogisticsDocument(models.Model):
    DOC_TYPES = [
        ('invoice', 'Factura Comercial'),
        ('packing_list', 'Packing List'),
        ('pedimento', 'Pedimento Aduanal'),
        ('contract', 'Contrato'),
        ('insurance', 'Seguro'),
        ('photo', 'Fotografía Carga/Entrega'),
        ('other', 'Otro'),
    ]
    
    order = models.ForeignKey(LogisticsOrder, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to='logistics/%Y/%m/')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES, verbose_name="Tipo de Documento")
    description = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_doc_type_display()} - {self.order.shipment_id}"
