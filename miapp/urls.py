from django.urls import path, include  
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, ProductoViewSet, CarritoViewSet, PedidoViewSet,
    DetallePedidoViewSet, FavoritoViewSet, UserViewSet, UsuarioActualView,
    CheckoutView  
)

# 🔀 Enrutador de vistas REST
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'carrito', CarritoViewSet, basename='carrito')
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'detalles-pedido', DetallePedidoViewSet, basename='detallepedido')
router.register(r'favoritos', FavoritoViewSet, basename='favorito')
router.register(r'usuarios', UserViewSet, basename='usuario')

# 🌐 Rutas finales de la API
urlpatterns = [
    path('', include(router.urls)),
    path('usuario-actual/', UsuarioActualView.as_view(), name='usuario_actual'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),  # ✅ Nueva ruta
]
