from django.contrib import admin
from pedido.models import Pedido, ItemPedido



class ItemPedidoInLine(admin.TabularInline):
    model = ItemPedido
    extra = 1



class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInLine
    ]



admin.site.register(Pedido, PedidoAdmin)  # Registrando Pedido(MODEL) e PedidoAdmin(MODEL ADMIN)
admin.site.register(ItemPedido)  # Registrando o model ItemPedido que está em models.py deste app(pedido)