# inventario_de_obra/models.py
from django.db import models
from rubros.models import Material
from contabilidad.models import SRIFactura
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from datetime import date
import re
import unicodedata
    
# class Inventario(models.Model):
#     material = models.OneToOneField(Material, on_delete=models.CASCADE, related_name="inventario")

#     @property
#     def stock_actual(self):
#         # Sumar todas las cantidades de entrada
#         entradas_total = self.material.entradas.aggregate(total=Sum('cantidad'))['total'] or 0
#         # Sumar todas las cantidades de salida
#         salidas_total = self.material.salidas.aggregate(total=Sum('cantidad'))['total'] or 0
#         # Calcular el stock actual
#         return entradas_total - salidas_total

#     def __str__(self):
#         unidad = self.material.unidad.abreviatura if self.material.unidad else ""
#         return f"Inventario de {self.material.nombre} - Stock Actual: {self.stock_actual} {unidad}"

# Modelo actualizado para Entrada de Inventario
class EntradaInventario(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="entradas")
    factura = models.ForeignKey(SRIFactura, on_delete=models.CASCADE, related_name="entrada_inventario", null=True, blank=True) 
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, help_text="Descripción de la entrada")
    fecha = models.DateField(verbose_name='Fecha de entradada del material', default=date.today)
    
    def __str__(self):
        return f"Entrada de {self.cantidad} {self.material.unidad} de {self.material.nombre}"
        

class SalidaInventario(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="salidas")
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, help_text="Descripción del uso")


    def __str__(self):
        return f"Salida de {self.cantidad} {self.material.unidad} de {self.material.nombre}"

class Inventario(models.Model):
    material = models.OneToOneField(Material, on_delete=models.CASCADE, related_name="inventario")
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    def actualizar_stock(self):
        # Sumar todas las cantidades de entrada
        entradas_total = self.material.entradas.aggregate(total=Sum('cantidad'))['total'] or 0
        # Sumar todas las cantidades de salida
        salidas_total = self.material.salidas.aggregate(total=Sum('cantidad'))['total'] or 0
        # Calcular el stock actual
        self.stock_actual = entradas_total - salidas_total
        self.save()

    def __str__(self):
        unidad = self.material.unidad.abreviatura if self.material.unidad else ""
        return f"Inventario de {self.material.nombre} - Stock Actual: {self.stock_actual} {unidad}"


@receiver(post_save, sender=EntradaInventario)
def crear_actualizar_inventario(sender, instance, created, **kwargs):
    # Obtén o crea un inventario para el material relacionado
    inventario, _ = Inventario.objects.get_or_create(material=instance.material)
    # Actualiza el stock del inventario
    inventario.actualizar_stock()

@receiver(post_delete, sender=EntradaInventario)
def actualizar_inventario_despues_eliminar(sender, instance, **kwargs):
    # Actualiza el stock después de eliminar una entrada
    if hasattr(instance.material, 'inventario'):
        instance.material.inventario.actualizar_stock()

@receiver(post_save, sender=SalidaInventario)
@receiver(post_delete, sender=SalidaInventario)
def actualizar_inventario_salida(sender, instance, **kwargs):
    if hasattr(instance.material, 'inventario'):
        instance.material.inventario.actualizar_stock()

