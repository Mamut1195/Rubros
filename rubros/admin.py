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
# from inventario_de_obra.admin import EntradaInventarioInline, SalidaInventarioInline  # Import the inlines


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
    list_display = ('nombre', 'unidad', 'costo_por_unidad')
    search_fields = ('nombre',)
    list_filter = ('unidad', 'nombre')
#     inlines = [EntradaInventarioInline, SalidaInventarioInline] 

# # Re-register Material with the updated MaterialAdmin configuration
# admin.site.unregister(Material)  # Unregister the original admin registration
# admin.site.register(Material, MaterialAdmin)  # Register with the updated admin

# Registrar el modelo Herramienta
@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'unidad', 'costo_por_unidad',)
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
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Calcular el costo total y agregarlo como un atributo de contexto en el formset
        if obj:
            total_costo = obj.calcular_costo_total_materiales()
            formset.total_costo = total_costo
        else:
            formset.total_costo = 0
        return formset


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
    list_display = ('nombre', 'codigo', 'codigo_personalizado', 'descripcion', 'unidad', 'get_costo_total_materiales', 
    'get_costo_total_herramientas', 'get_costo_total_mano_de_obra', 'indirectos',)
    search_fields = ('nombre', 'codigo', 'codigo_personalizado', 'get_costo_total_mano_de_obra',)
    list_filter = ('codigo',)
    readonly_fields = ('get_costo_total_materiales', 'get_costo_total_herramientas','get_costo_total_mano_de_obra',)
    inlines = [RubroMaterialInline, RubroHerramientaInline,  RubroManoObraInline]

    # Método para mostrar el costo total de materiales en el admin
    def get_costo_total_materiales(self, obj):
        return obj.calcular_costo_total_materiales()

    get_costo_total_materiales.short_description = 'Costo Total Materiales'

    # Método para mostrar el costo total de las herramientas en el admin
    def get_costo_total_herramientas(self, obj):
        return obj.calcular_costo_total_herramientas()

    get_costo_total_herramientas.short_description = 'Costo Total Herramientas'

        # Método para mostrar el costo total de las herramientas en el admin
    def get_costo_total_mano_de_obra(self, obj):
        return obj.calcular_costo_total_mano_de_obra()

    get_costo_total_mano_de_obra.short_description = 'Costo Total Mano de obra'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        extra_context = extra_context or {}
        if obj:
            extra_context['total_costo_materiales'] = obj.calcular_costo_total_materiales()
            extra_context['total_costo_herramientas'] = obj.calcular_costo_total_herramientas()
            extra_context['total_costo_mano_obra'] = obj.calcular_costo_total_mano_de_obra()
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    class Media:
        js = ('js/rubromateriales.js', 'js/rubroherramientas.js', 'js/rubromanodeobra.js', 'js/costo_total_rubro.js')