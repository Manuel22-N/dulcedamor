"""
URL configuration for dulcedamor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dulcedamor.views.dashboard_views import dashboard_view
from dulcedamor.views.configuration_views import configuration_view
from dulcedamor.views.usuarios_views import gestionar_usuarios, editar_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/configuration/', configuration_view, name='configuration'),
    # Rutas para gestionar usuarios
    path('gestionar-usuarios/', gestionar_usuarios, name='gestionar_usuarios'),
    path('gestionar-usuarios/editar/<int:usuario_id>/', editar_usuario, name='editar_usuario'),
]
