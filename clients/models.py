from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre / Razón Social")
    tax_id = models.CharField(max_length=50, verbose_name="RFC / Tax ID", unique=True)
    address = models.TextField(verbose_name="Dirección Fiscal", blank=True)
    
    # Contact Info
    contact_name = models.CharField(max_length=100, verbose_name="Nombre de Contacto", blank=True)
    email = models.EmailField(verbose_name="Correo Electrónico", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True)
    
    payment_terms = models.CharField(max_length=100, verbose_name="Condiciones de Pago", blank=True, help_text="Ej. 30 días, Contado")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['name']

    def __str__(self):
        return self.name
