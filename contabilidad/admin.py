from django.contrib import admin
from .models import SRIFactura

@admin.register(SRIFactura)
class SRIFacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'nombre', 'nombre_comercial', 'ruc', 'numero_autorizacion')
    search_fields = ('ruc', 'numero_factura', 'numero_autorizacion', 'nombre', 'nombre_comercial')
    list_filter = ( 'nombre_comercial',)






