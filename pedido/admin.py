from django.contrib import admin
from .models import ItemPedido, Pedido


class ItemPedidoInline(admin.StackedInline):
    model = ItemPedido
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    inlines = [ItemPedidoInline]


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)
