from django.db import models
import uuid

# Modelo para Salarios Mínimos por Ley
class SalarioMinimo(models.Model):
    cargo = models.CharField(max_length=255)  # Nombre del cargo (ej. Albañil, Electricista)
    salario_horario_minimo = models.DecimalField(max_digits=10, decimal_places=2)  # Salario mínimo por hora

    class Meta:
        verbose_name = "Salario minimo"
        verbose_name_plural = "Salarios minimos"

    def __str__(self):
        return f"{self.cargo} - {self.salario_horario_minimo} por hora"

# Modelo para Unidades de Medida
class Unidad(models.Model):
    nombre = models.CharField(max_length=100)
    abreviatura = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"

# Modelo para Rubros de Construcción
class Rubro(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=50, unique=True, blank=True)
    codigo_personalizado = models.CharField(max_length=50, blank=True, null=True)
    unidad = models.ForeignKey('Unidad', on_delete=models.SET_NULL, null=True) 

    #Método para sumar todos los costos de RubroMaterial
    def calcular_costo_total_rubros(self):
        total = 0
        for rubro_material in self.rubromaterial_set.all():
            total += rubro_material.costo_total
        return total

    def __str__(self):
        return self.nombre


# Modelo para Materiales
class Material(models.Model):
    nombre = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True)
    costo_por_unidad = models.DecimalField(max_digits=10, decimal_places=2, editable=True, verbose_name="Costo unitario", default=0.00)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ['nombre']  # Ordena por el campo 'nombre'

    def __str__(self):
        return f"{self.nombre} - {self.unidad}"

# Modelo intermedio para calcular costos de materiales en el rubro
class RubroMaterial(models.Model):
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad_requerida = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad')

    @property
    def costo_unitario(self):
        return self.material.costo_por_unidad
    
    @property
    def costo_total(self):
        return self.cantidad_requerida * self.material.costo_por_unidad


# Modelo para Herramientas
class Herramienta(models.Model):
    nombre = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField()
    costo_por_unidad = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nombre}"

# Modelo intermedio para calcular costos de herramientas en el rubro
class RubroHerramienta(models.Model):
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    cantidad_requerida = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad')

    @property
    def costo_unitario(self):
        return self.herramienta.costo_por_unidad
    
    @property
    def costo_total(self):
        return self.cantidad_requerida * self.herramienta.costo_por_unidad


# Modelo para Mano de Obra
class ManoObra(models.Model):
    cargo = models.CharField(max_length=15, blank=True, null=True)
    salario_minimo = models.ForeignKey(SalarioMinimo, on_delete=models.SET_NULL, null=True)
    numero_de_contacto = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = "Mano de obra"
        verbose_name_plural = "Mano de obra"

    def __str__(self):
        return f"{self.salario_minimo.cargo} "

# Modelo intermedio para calcular costos de mano de obra en el rubro
class RubroManoObra(models.Model):
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    mano_obra = models.ForeignKey(ManoObra, on_delete=models.CASCADE)
    cantidad_horas_requeridas = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def costo_unitario(self):
        return self.mano_obra.salario_minimo.salario_horario_minimo
    
    @property
    def costo_total(self):
        return self.cantidad_horas_requeridas * self.mano_obra.salario_minimo.salario_horario_minimo
