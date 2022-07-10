from django.urls import path
from . import views


app_name = 'pedido'  # pedido:pay

urlpatterns = [
    path('', views.Pay.as_view(), name='pay'),
    path('closeorder/', views.CloseOrder.as_view(), name='closeorder'),
    path('details/', views.Details.as_view(), name='details'),
]