from django.db import models

# Create your models here.


class Personal(models.Model):
    nombre = models.CharField(max_length=255)
    cargo = models.ForeignKey(
        'rubros.ManoObra',  # Referencia al modelo ManoObra usando una cadena
        on_delete=models.SET_NULL,
        null=True,
        related_name="personal"
    )
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Personal"
        verbose_name_plural = "Personal"

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"

class RegistroAsistencia(models.Model):
    empleado = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField()
    presente = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)


    @property
    def sueldo(self):
        # Devuelve el sueldo del empleado asociado
        return self.empleado.sueldo

    def __str__(self):
        return f"Asistencia de {self.empleado.nombre} - {self.fecha}"

