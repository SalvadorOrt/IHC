from django.contrib import admin
from django.utils.html import format_html
from miapp.models import Categoria, Producto, Carrito, Pedido, DetallePedido, Favorito


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    exclude = ('vendedor',)
    readonly_fields = ('vista_previa',)
    list_display = ('id', 'nombre', 'precio', 'categoria', 'stock', 'vendedor', 'miniatura')
    list_filter = ('categoria',)
    search_fields = ('nombre',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(vendedor=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.vendedor = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser and obj.vendedor != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and not request.user.is_superuser and obj.vendedor != request.user:
            return False
        return super().has_delete_permission(request, obj)

    def has_module_permission(self, request):
        return True

    def miniatura(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: contain;" />', obj.imagen.url)
        return "(Sin imagen)"
    miniatura.short_description = 'Miniatura'

    def vista_previa(self, obj):
        if obj.imagen:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" width="200" style="object-fit: contain;" /></a>',
                obj.imagen.url
            )
        return "(Sin imagen)"
    vista_previa.short_description = 'Vista Previa'


class BaseUserRestrictedAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(usuario=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser and obj.usuario != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and not request.user.is_superuser and obj.usuario != request.user:
            return False
        return super().has_delete_permission(request, obj)

    def has_module_permission(self, request):
        return True


@admin.register(Carrito)
class CarritoAdmin(BaseUserRestrictedAdmin):
    list_display = ('id', 'usuario', 'producto', 'cantidad')


@admin.register(Pedido)
class PedidoAdmin(BaseUserRestrictedAdmin):
    list_display = ('id', 'usuario', 'total', 'estado')


@admin.register(Favorito)
class FavoritoAdmin(BaseUserRestrictedAdmin):
    list_display = ('id', 'usuario', 'producto')


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'producto', 'cantidad', 'precio_unitario')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(pedido__usuario=request.user)

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser and obj.pedido.usuario != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and not request.user.is_superuser and obj.pedido.usuario != request.user:
            return False
        return super().has_delete_permission(request, obj)

    def has_module_permission(self, request):
        return True
