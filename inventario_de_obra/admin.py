# Register your models here.
# inventario_de_obra/admin.py

from django.contrib import admin
from .models import Inventario, EntradaInventario, SalidaInventario, Proveedor, Factura
from rubros.models import Material
from django.db import models

# # Inline para mostrar Entradas de Inventario dentro de la vista del Material en el inventario
# class EntradaInventarioInline(admin.TabularInline):
#     model = EntradaInventario
#     extra = 1
#     readonly_fields = ('fecha',)
#     fields = ('fecha', 'cantidad', 'descripcion')

# # Inline para mostrar Salidas de Inventario dentro de la vista del Material en el inventario
# class SalidaInventarioInline(admin.TabularInline):
#     model = SalidaInventario
#     extra = 1
#     readonly_fields = ('fecha',)
#     fields = ('fecha', 'cantidad', 'descripcion')

# Admin para Proveedor
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre_comercial', 'ruc', 'direccion')
    search_fields = ('nombre_comercial', 'ruc')

# Admin para Factura
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'proveedor', 'fecha_emision', 'monto_total')
    list_filter = ('proveedor', 'fecha_emision')
    search_fields = ('numero', 'proveedor__nombre_comercial')

# Registro de los modelos EntradaInventario y SalidaInventario para ver el historial completo
@admin.register(EntradaInventario)
class EntradaInventarioAdmin(admin.ModelAdmin):
    list_display = ('material', 'proveedor', 'factura', 'fecha', 'cantidad', 'descripcion')
    list_filter = ('proveedor', 'factura', 'material')
    search_fields = ('material__nombre', 'proveedor__nombre_comercial', 'factura__numero')
    readonly_fields = ('fecha','get_unidad',)


    # Método para mostrar la unidad en el listado
    def get_unidad(self, obj):
        return obj.material.unidad.abreviatura if obj.material.unidad else ""
    get_unidad.short_description = 'Unidad'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "material":
            kwargs["queryset"] = Material.objects.all()
            form_field = super().formfield_for_foreignkey(db_field, request, **kwargs)
            # Modificar las opciones para incluir la unidad en el texto
            form_field.choices = [
                (material.id, f"{material.nombre} ({material.unidad.abreviatura if material.unidad else 'N/A'})")
                for material in Material.objects.all()
            ]
            return form_field
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(SalidaInventario)
class SalidaInventarioAdmin(admin.ModelAdmin):
    list_display = ('material', 'fecha', 'cantidad', 'get_unidad', 'descripcion')
    list_filter = ('material',)
    search_fields = ('material__nombre', 'descripcion')
    readonly_fields = ('fecha','get_unidad',)
    

        # Move the fields to display `get_unidad` before `descripcion`
    fieldsets = (
        (None, {
            'fields': ('material', 'fecha', 'cantidad', 'get_unidad', 'descripcion')
        }),
    )

    # Método para mostrar la unidad en el listado
    def get_unidad(self, obj):
        return obj.material.unidad.abreviatura if obj.material.unidad else ""
    get_unidad.short_description = 'Unidad'


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('material', 'stock_actual', 'get_unidad')
    search_fields = ('material__nombre',)
    readonly_fields = ('stock_actual',)

    def get_queryset(self, request):
        # Muestra todos los materiales que tienen entradas o salidas
        qs = super().get_queryset(request)
        return qs.filter(models.Q(material__entradas__isnull=False) | models.Q(material__salidas__isnull=False)).distinct()

    def get_unidad(self, obj):
        return obj.material.unidad.abreviatura if obj.material.unidad else ""
    get_unidad.short_description = 'Unidad'



