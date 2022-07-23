from django.urls import path
from . import views


app_name = 'pedido'  # pedido:pay

urlpatterns = [
    path('pay/<int:pk>', views.Pay.as_view(), name='pay'),
    path('saveorder/', views.SaveOrder.as_view(), name='save_order'),
    path('list/', views.List.as_view(), name='list'),
    path('details/', views.Details.as_view(), name='details'),
]