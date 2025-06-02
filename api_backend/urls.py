from django.conf import settings 
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from miapp.views import UsuarioActualView  # 👈 importar tu vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('miapp.urls')),

    # 🔐 Rutas JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 👤 Ruta para obtener datos del usuario logueado
    path('api/usuario-actual/', UsuarioActualView.as_view(), name='usuario_actual'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
