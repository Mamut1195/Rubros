from django.contrib import admin
from .models import (
    SalarioMinimo,
    Unidad,
    Rubro,
    Material,
    Herramienta,
    ManoObra,
    RubroMaterial,
    RubroHerramienta,
    RubroManoObra
)

# Registrar el modelo SalarioMinimo
@admin.register(SalarioMinimo)
class SalarioMinimoAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'salario_horario_minimo')
    search_fields = ('cargo',)

# Registrar el modelo Unidad
@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'abreviatura')
    search_fields = ('nombre', 'abreviatura')

# Registrar el modelo Material
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'unidad', 'cantidad', 'costo_por_unidad')
    search_fields = ('nombre',)
    list_filter = ('unidad', 'nombre')

# Registrar el modelo Herramienta
@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'costo_por_unidad',)
    search_fields = ('nombre', )
    list_filter = ('nombre',)

# Registrar el modelo ManoObra
@admin.register(ManoObra)
class ManoObraAdmin(admin.ModelAdmin):
    list_display = ( 'cargo','salario_minimo', 'numero_de_contacto')
    search_fields = ('nombre', 'cargo')
    list_filter = ('salario_minimo', 'cargo')


# Inline para RubroMaterial
class RubroMaterialInline(admin.TabularInline):
    model = RubroMaterial
    extra = 1
    fields = ('material', 'cantidad_requerida', 'costo_unitario', 'costo_total')
    readonly_fields = ('costo_unitario', 'costo_total')

    # Método para obtener el valor de la propiedad costo_unitario
    def costo_unitario(self, obj):
        return obj.costo_unitario

    # Método para obtener el valor del costo total (cantidad * costo unitario)
    def costo_total(self, obj):
        return obj.costo_total


# Inline para RubroHerramienta
class RubroHerramientaInline(admin.TabularInline):
    model = RubroHerramienta
    extra = 1
    fields = ('herramienta', 'cantidad_requerida', 'costo_unitario', 'costo_total')
    readonly_fields = ('costo_unitario', 'costo_total')

    # Método para obtener el valor de la propiedad costo_unitario
    def costo_unitario(self, obj):
        return obj.costo_unitario

    # Método para obtener el valor del costo total (cantidad * costo unitario)
    def costo_total(self, obj):
        return obj.costo_total

# Inline para RubroManoObra
class RubroManoObraInline(admin.TabularInline):
    model = RubroManoObra
    extra = 1
    fields = ('mano_obra', 'cantidad_horas_requeridas', 'costo_unitario', 'costo_total')
    readonly_fields = ('costo_unitario', 'costo_total')

    # Método para obtener el valor de la propiedad costo_unitario
    def costo_unitario(self, obj):
        return obj.costo_unitario

    # Método para obtener el valor del costo total (cantidad de horas * costo unitario)
    def costo_total(self, obj):
        return obj.costo_total
    


# Registrar el modelo Rubro con los inlines correspondientes
@admin.register(Rubro)
class RubroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'codigo_personalizado', 'descripcion', 'unidad')
    search_fields = ('nombre', 'codigo', 'codigo_personalizado')
    list_filter = ('codigo',)
    inlines = [RubroMaterialInline, RubroHerramientaInline,  RubroManoObraInline]

    # Método para mostrar el costo total de todos los materiales, herramientas, equipos y mano de obra
    def calcular_costo_total(self, obj):
        total = obj.calcular_costo_total_rubros()
        return total
