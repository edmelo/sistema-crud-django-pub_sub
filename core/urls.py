"""
URL configuration for sistema_crud project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Home page
    path('', TemplateView.as_view(template_name='base/home.html'), name='home'),

    # Apps URLs
    path('usuarios/', include('apps.usuarios.urls')),
    path('produtos/', include('apps.produtos.urls')),
    path('pedidos/', include('apps.pedidos.urls')),

    # API URLs
    path('api/usuarios/', include('apps.usuarios.api_urls')),
    path('api/produtos/', include('apps.produtos.api_urls')),
    path('api/pedidos/', include('apps.pedidos.api_urls')),

    # DRF Browsable API
    path('api-auth/', include('rest_framework.urls')),
]

# Servir arquivos de média em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
