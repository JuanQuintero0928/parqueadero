"""parqueadero URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login
from parking.views import Inicio

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('', Inicio.as_view(), name='inicio'),
    path('', login_required(Inicio.as_view()), name='inicio'),
    path('accounts/login/',LoginView.as_view(template_name='login.html'), name='login'),
    path('parking/',include(('parking.urls','parking'))),
    path("reportes/", include(('reportes.urls','reportes'))),
    path('logout/', logout_then_login, name='logout'),
]
