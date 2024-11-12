# inventario_de_obra/models.py
from django.db import models
from rubros.models import Material  # Importa el modelo Material de la app rubros
from django.db.models import Sum

class EntradaInventario(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="entradas")
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, help_text="Descripción de la entrada o proveedor")

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

    @property
    def stock_actual(self):
        # Sumar todas las cantidades de entrada
        entradas_total = self.material.entradas.aggregate(total=Sum('cantidad'))['total'] or 0
        # Sumar todas las cantidades de salida
        salidas_total = self.material.salidas.aggregate(total=Sum('cantidad'))['total'] or 0
        # Calcular el stock actual
        return entradas_total - salidas_total

    def __str__(self):
        unidad = self.material.unidad.abreviatura if self.material.unidad else ""
        return f"Inventario de {self.material.nombre} - Stock Actual: {self.stock_actual} {unidad}"



