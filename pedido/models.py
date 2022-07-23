from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):
    class Meta:
        verbose_name_plural = 'Pedidos'
        verbose_name = ' Pedido'
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ("A", "Aprovado"),
            ("C", "Criado"),
            ("R", "Reprovado"),
            ("P", "Pendente"),
            ("E", "Enviado"),
            ("F", "Finalizado"),
        ),
    )


    def __str__(self) -> str:
        return f'Pedido N. {self.pk}'


class ItemPedido(models.Model):
    class Meta:
        verbose_name_plural = "Items do pedido"
        verbose_name = ' Item do pedido'


    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=100, verbose_name='Variação')
    variacao_id = models.PositiveIntegerField(verbose_name='Variação id')
    preco = models.FloatField(verbose_name='preço')
    preco_promocinal = models.FloatField(default=0, verbose_name='preço promocional')
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)


    def __str__(self) -> str:
        return f'Item do {self.pedido}'
