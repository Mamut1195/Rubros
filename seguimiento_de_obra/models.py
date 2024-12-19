from django.db import models
from rubros.models import Rubro, ManoObra, Herramienta

class SeguimientoDiario(models.Model):
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE, related_name="seguimientos_diarios")
    fecha = models.DateField(verbose_name="Fecha del seguimiento")
    observaciones = models.TextField(blank=True, null=True, help_text="Observaciones generales del día")

    class Meta:
        verbose_name = "Seguimiento Diario"
        verbose_name_plural = "Seguimiento Diario"

    def __str__(self):
        return f"{self.rubro.nombre} - {self.fecha}"


class ManoObraSeguimiento(models.Model):
    seguimiento_diario = models.ForeignKey(SeguimientoDiario, on_delete=models.CASCADE, related_name="mano_obra_seguimiento")
    mano_obra = models.ForeignKey(ManoObra, on_delete=models.CASCADE, related_name="seguimientos")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad trabajada")
    rendimiento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Rendimiento diario")
    costo_horario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo horario")

    @property
    def costo_total(self):
        # Asegúrate de que cantidad y costo_horario no sean None antes de calcular
        if self.cantidad is not None and self.costo_horario is not None:
            return self.cantidad * self.costo_horario
        return 0  # Devuelve 0 si alguno es None

    class Meta:
        verbose_name = "Seguimiento de Mano de Obra"
        verbose_name_plural = "Seguimientos de Mano de Obra"

    def __str__(self):
        return f"{self.mano_obra.cargo} - {self.seguimiento_diario.fecha}"


class HerramientaSeguimiento(models.Model):
    seguimiento_diario = models.ForeignKey(SeguimientoDiario, on_delete=models.CASCADE, related_name="herramientas_seguimiento")
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE, related_name="seguimientos")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad utilizada")
    rendimiento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Rendimiento diario")
    costo_horario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo horario")

    @property
    def costo_total(self):
        # Asegúrate de que cantidad y costo_horario no sean None antes de calcular
        if self.cantidad is not None and self.costo_horario is not None:
            return self.cantidad * self.costo_horario
        return 0  # Devuelve 0 si alguno es None

    class Meta:
        verbose_name = "Seguimiento de Herramientas"
        verbose_name_plural = "Seguimientos de Herramientas"

    def __str__(self):
        return f"{self.herramienta.nombre} - {self.seguimiento_diario.fecha}"
