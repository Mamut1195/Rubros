from django.db import models
import uuid
from django.core.exceptions import ValidationError
import re
from unidecode import unidecode 

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

    def clean(self):
        # Limpieza de espacios, normalización y eliminación de tildes
        self.nombre = unidecode(re.sub(r'\s+', ' ', self.nombre.strip().lower()))  # Normaliza y elimina espacios y tildes
        if self.abreviatura:
            self.abreviatura = unidecode(re.sub(r'\s+', ' ', self.abreviatura.strip().lower()))  # Normaliza y elimina espacios y tildes

        # Validar unicidad del nombre
        if Unidad.objects.exclude(id=self.id).filter(nombre=self.nombre).exists():
            raise ValidationError({'nombre': 'Ya existe una unidad con este nombre.'})

        # Validar unicidad de la abreviatura (si está presente)
        if self.abreviatura and Unidad.objects.exclude(id=self.id).filter(abreviatura=self.abreviatura).exists():
            raise ValidationError({'abreviatura': 'Ya existe una unidad con esta abreviatura.'})

    def save(self, *args, **kwargs):
        # Llama a clean para garantizar que se apliquen las validaciones antes de guardar
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"



# Modelo para Materiales
class Material(models.Model):
    nombre = models.CharField(max_length=255)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True)
    costo_por_unidad = models.DecimalField(max_digits=10, decimal_places=2, editable=True, verbose_name="Costo unitario", default=0.00)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ['nombre']  # Ordena por el campo 'nombre'
    
    def clean(self):
        # Limpieza de espacios, normalización y eliminación de tildes
        cleaned_name = re.sub(r'\s+', ' ', self.nombre.strip())  # Elimina espacios extra
        normalized_name = unidecode(cleaned_name).capitalize()  # Elimina tildes y normaliza como título

        # Verifica unicidad insensible a mayúsculas/minúsculas, tildes y espacios
        if Material.objects.filter(nombre__iexact=normalized_name).exclude(pk=self.pk).exists():
            raise ValidationError(f"Ya existe un material con el nombre '{normalized_name}'.")

        # Asigna el nombre limpio y normalizado
        self.nombre = normalized_name

    def save(self, *args, **kwargs):
        # Normalizar el texto del nombre
        self.full_clean()  # Llama a clean() para aplicar validaciones antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


# Modelo para Herramientas
class Herramienta(models.Model):
    nombre = models.CharField(max_length=255)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True)
    costo_por_unidad = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nombre}"

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


# Modelo para Rubros de Construcción
class Rubro(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=50, unique=True, blank=True)
    codigo_personalizado = models.CharField(max_length=50, blank=True, null=True)
    unidad = models.ForeignKey('Unidad', on_delete=models.SET_NULL, null=True) 
    indirectos = models.DecimalField(max_digits=5, decimal_places=2, default=20.00,
                                      verbose_name="Indirectos (%)")


    # Método para calcular el costo total de todos los materiales relacionados
    def calcular_costo_total_materiales(self):
        return sum(material.costo_total for material in self.rubromaterial_set.all())

        # Método para calcular el costo total de todos las herramientas relacionadas
    def calcular_costo_total_herramientas(self):
        return sum(herramienta.costo_total for herramienta in self.rubroherramienta_set.all())

            # Método para calcular el costo total de todos las herramientas relacionadas
    def calcular_costo_total_mano_de_obra(self):
        return sum(manoobra.costo_total for manoobra in self.rubromanoobra_set.all())
    
    def __str__(self):
        return self.nombre

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
        return self.cantidad_horas_requeridas * self.costo_unitario
