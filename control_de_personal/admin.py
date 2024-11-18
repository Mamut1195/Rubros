from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Personal, RegistroAsistencia
from django.db import models

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'sueldo', 'fecha_ingreso', 'activo')
    search_fields = ('nombre', 'cargo')
    list_filter = ('activo', 'fecha_ingreso')


@admin.action(description='Calcular suma de sueldos seleccionados')
def calcular_suma_sueldos(modeladmin, request, queryset):
    total_sueldos = queryset.aggregate(total=models.Sum('empleado__sueldo'))['total']
    modeladmin.message_user(request, f"El total de los sueldos seleccionados es: {total_sueldos}")

@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'fecha', 'presente', 'get_sueldo', 'observaciones')
    list_filter = ('empleado', 'fecha', 'presente')
    search_fields = ('empleado__nombre', 'observaciones')
    actions = [calcular_suma_sueldos]  # Añade la acción

    def get_sueldo(self, obj):
        return obj.sueldo
    get_sueldo.short_description = 'Sueldo'