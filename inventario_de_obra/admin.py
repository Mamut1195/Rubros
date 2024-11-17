# Register your models here.
# inventario_de_obra/admin.py

from django.contrib import admin
from .models import Inventario, EntradaInventario, SalidaInventario



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

# Registro de los modelos EntradaInventario y SalidaInventario para ver el historial completo
@admin.register(EntradaInventario)
class EntradaInventarioAdmin(admin.ModelAdmin):
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


# Admin para Inventario
@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('material', 'stock_actual', 'get_unidad')
    search_fields = ('material_nombre',)
    readonly_fields = ('stock_actual',)

    def get_unidad(self, obj):
        return obj.material.unidad.abreviatura if obj.material.unidad else ""
    
    get_unidad.short_description = 'Unidad'



