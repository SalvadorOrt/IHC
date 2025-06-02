from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Categoria, Producto, Carrito, Pedido, DetallePedido, Favorito
from .serializers import (
    CategoriaSerializer, ProductoSerializer, CarritoSerializer,
    PedidoSerializer, DetallePedidoProductoSerializer,
    FavoritoSerializer, UserSerializer
)
from rest_framework.exceptions import ValidationError

# ✅ Usuarios
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Usuario actual
class UsuarioActualView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# ✅ Categorías
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]

# ✅ Productos
class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_authenticated:
            return Producto.objects.exclude(vendedor=usuario)
        return Producto.objects.all()

    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user)

# ✅ Carrito con validación de duplicados
class CarritoViewSet(viewsets.ModelViewSet):
    serializer_class = CarritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Carrito.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        usuario = self.request.user
        producto = serializer.validated_data['producto']
        cantidad_nueva = serializer.validated_data['cantidad']

        try:
            existente = Carrito.objects.get(usuario=usuario, producto=producto)
            cantidad_total = existente.cantidad + cantidad_nueva

            if cantidad_total > producto.stock:
                raise ValidationError({
                    'cantidad': f'La cantidad total solicitada ({cantidad_total}) excede el stock disponible ({producto.stock}).'
                })

            existente.cantidad = cantidad_total
            existente.save()
        except Carrito.DoesNotExist:
            if cantidad_nueva > producto.stock:
                raise ValidationError({
                    'cantidad': f'La cantidad solicitada ({cantidad_nueva}) excede el stock disponible ({producto.stock}).'
                })
            serializer.save(usuario=usuario)

# ✅ Pedidos
class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)

# ✅ Detalles del Pedido
class DetallePedidoViewSet(viewsets.ModelViewSet):
    serializer_class = DetallePedidoProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DetallePedido.objects.filter(pedido__usuario=self.request.user)

# ✅ Favoritos
class FavoritoViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

# ✅ Checkout con validación de stock
class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        usuario = request.user
        carrito_items = Carrito.objects.filter(usuario=usuario)

        if not carrito_items.exists():
            return Response({'error': 'El carrito está vacío'}, status=status.HTTP_400_BAD_REQUEST)

        # Validar stock
        for item in carrito_items:
            if item.cantidad > item.producto.stock:
                return Response({
                    'error': f'No hay suficiente stock para {item.producto.nombre}.'
                }, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.producto.precio * item.cantidad for item in carrito_items)

        pedido = Pedido.objects.create(usuario=usuario, total=total, estado='pendiente')

        for item in carrito_items:
            DetallePedido.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio
            )
            producto = item.producto
            producto.stock -= item.cantidad
            producto.save()

        carrito_items.delete()

        return Response({'mensaje': 'Compra realizada con éxito'}, status=status.HTTP_201_CREATED)
