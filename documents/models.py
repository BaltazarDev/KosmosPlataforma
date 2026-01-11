from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Document(models.Model):
    """
    Generic document model that can be attached to any other model 
    (Client, Provider, PurchaseOrder, LogisticsOrder, etc.)
    """
    title = models.CharField(max_length=100, verbose_name="Título del Documento")
    file = models.FileField(upload_to='documents/%Y/%m/')
    description = models.TextField(blank=True)
    
    # Generic Relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
