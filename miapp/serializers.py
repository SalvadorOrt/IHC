from rest_framework import serializers
from .models import Categoria, Producto, Carrito, Pedido, DetallePedido, Favorito
from django.contrib.auth.models import User

# ✅ Usuario con nombre y apellido
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# ✅ Categorías
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

# ✅ Productos
class ProductoSerializer(serializers.ModelSerializer):
    vendedor = UserSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'imagen', 'categoria', 'stock', 'vendedor']

# ✅ Carrito
class CarritoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'producto', 'cantidad']

    def validate(self, data):
        # Obtenemos el producto desde data o desde la instancia (en caso de PATCH)
        producto = data.get('producto') or getattr(self.instance, 'producto', None)
        cantidad = data.get('cantidad', getattr(self.instance, 'cantidad', None))

        if producto and cantidad is not None and cantidad > producto.stock:
            raise serializers.ValidationError({
                'cantidad': f'La cantidad solicitada ({cantidad}) excede el stock disponible ({producto.stock}).'
            })

        return data

    def update(self, instance, validated_data):
        nueva_cantidad = validated_data.get('cantidad', instance.cantidad)
        if nueva_cantidad > instance.producto.stock:
            raise serializers.ValidationError({
                'cantidad': f'La cantidad solicitada ({nueva_cantidad}) excede el stock disponible ({instance.producto.stock}).'
            })

        return super().update(instance, validated_data)

# ✅ Detalle de pedidos
class DetallePedidoProductoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'cantidad', 'precio_unitario']

# ✅ Pedidos con detalles anidados
class PedidoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    detalles = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'total', 'estado', 'detalles']

    def get_detalles(self, obj):
        detalles = DetallePedido.objects.filter(pedido=obj)
        return DetallePedidoProductoSerializer(detalles, many=True).data

# ✅ Favoritos
class FavoritoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

    class Meta:
        model = Favorito
        fields = ['id', 'usuario', 'producto']
