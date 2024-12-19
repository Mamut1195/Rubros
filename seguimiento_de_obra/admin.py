from django.contrib import admin
from .models import SeguimientoDiario, ManoObraSeguimiento, HerramientaSeguimiento

class ManoObraSeguimientoInline(admin.TabularInline):
    model = ManoObraSeguimiento
    extra = 1
    fields = ('mano_obra', 'cantidad', 'rendimiento', 'costo_horario', 'costo_total')
    readonly_fields = ('costo_total',)

class HerramientaSeguimientoInline(admin.TabularInline):
    model = HerramientaSeguimiento
    extra = 1
    fields = ('herramienta', 'cantidad', 'rendimiento', 'costo_horario', 'costo_total')
    readonly_fields = ('costo_total',)

@admin.register(SeguimientoDiario)
class SeguimientoDiarioAdmin(admin.ModelAdmin):
    list_display = ('rubro', 'fecha', 'observaciones')
    inlines = [ManoObraSeguimientoInline, HerramientaSeguimientoInline]
