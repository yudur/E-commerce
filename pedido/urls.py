from django.urls import path
from . import views


app_name = 'pedido'  # pedido:pay

urlpatterns = [
    path('', views.Pay.as_view(), name='pay'),
    path('saveorder/', views.SaveOrder.as_view(), name='save_order'),
    path('details/', views.Details.as_view(), name='details'),
]