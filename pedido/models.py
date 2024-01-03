from django.db import models
from django.contrib.auth.models import User


# A relação entre "Pedido" e "ItemPedido" é semelhante à relação entre uma lista de compras e 
# os itens individuais nessa lista. Se você fizer uma lista de compras, o papel do "Pedido" é a lista em si, 
# enquanto cada "ItemPedido" é um produto específico que você deseja comprar e que está na lista.
class Pedido(models.Model):
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Apago usuário --> apago também os pedidos que pertenciam à aquele usuário
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField()
    status = models.CharField(
        default='C', max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        )
    )

    def __str__(self):
        return f'Pedido Nº {self.pk}'



# Cada item está associado a um "Pedido" e representa um produto que o usuário deseja comprar
class ItemPedido(models.Model):
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # Quando um Pedido for deletado, deletar também os ItensPedidos
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do {self.pedido}'