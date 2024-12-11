from django.db import models
from django.core.exceptions import ValidationError
import re
from unidecode import unidecode
from datetime import date

class SRIFactura(models.Model):
    ruc = models.CharField(max_length=13, verbose_name="RUC", blank=False, null=False)
    numero_factura = models.CharField(max_length=50, verbose_name="Número de Factura", blank=False, null=False)
    numero_autorizacion = models.CharField(max_length=255, unique=True, verbose_name="Número de Autorización", blank=False, null=False)
    nombre = models.CharField(max_length=255, verbose_name="Nombre", blank=False, null=False)
    nombre_comercial = models.CharField(max_length=255, verbose_name="Nombre Comercial", blank=False, null=False, default='')
    fecha = models.DateField(verbose_name='Fecha de emisión de la factura', default=date.today)

    class Meta:
        verbose_name = "Factura SRI"
        verbose_name_plural = "Facturas SRI"

    def clean(self):
        # Limpieza y normalización de campos
        self.ruc = re.sub(r'\s+', '', self.ruc.strip())  # Elimina espacios
        if not re.match(r'^\d{13}$', self.ruc):
            raise ValidationError({'ruc': "El RUC debe tener exactamente 13 dígitos numéricos."})

        self.numero_factura = re.sub(r'\s+', '', self.numero_factura.strip())  # Elimina espacios
        self.numero_autorizacion = re.sub(r'\s+', '', self.numero_autorizacion.strip())  # Elimina espacios

        # Validar unicidad del número de autorización
        if SRIFactura.objects.exclude(id=self.id).filter(numero_autorizacion=self.numero_autorizacion).exists():
            raise ValidationError({'numero_autorizacion': "Ya existe una factura con este número de autorización."})

        # Validar unicidad del número de factura
        if SRIFactura.objects.exclude(id=self.id).filter(numero_factura=self.numero_factura).exists():
            raise ValidationError({'numero_factura': "Ya existe una factura con este número de factura."})

        # Normalizar nombres
        self.nombre = unidecode(re.sub(r'\s+', ' ', self.nombre.strip().title()))  # Normaliza y elimina espacios extras
        self.nombre_comercial = unidecode(re.sub(r'\s+', ' ', self.nombre_comercial.strip().title()))

    def save(self, *args, **kwargs):
        self.full_clean()  # Aplica validaciones antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_factura} - {self.nombre} ({self.ruc})"
