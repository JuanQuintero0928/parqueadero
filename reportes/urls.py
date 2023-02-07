from django.urls import path
from django.contrib.auth.decorators import login_required
from reportes.views import ListarFactura, GenerarInformeTotal, GenerarInformeTotalExcel, GenerarPdfFactura


urlpatterns = [
    path('listar_factura/', login_required(ListarFactura.as_view()), name='listar_factura'),
    path('generarFactura/<int:pk>', login_required(GenerarPdfFactura.as_view()), name='generarFactura'),
    path('generarInformeTotal/', login_required(GenerarInformeTotal.as_view()), name="generarInformeTotal"),
    path('generarInformeTotalExcel/', login_required(GenerarInformeTotalExcel.as_view()), name="generarInformeTotalExcel")
]
