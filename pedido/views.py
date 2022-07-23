from statistics import variance
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.http import HttpResponse
from django.contrib import messages

from produto.models import Variacao
from .models import Pedido, ItemPedido

from utils import utils


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:create')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs


class Pay(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pay.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'


class SaveOrder(View):
    template_name = 'pedido/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Log em sua conta ou cadaste-se antes de realisar sua compra.'
            )
            return redirect('perfil:create')
            
        if not self.request.session.get('carrinho'):
            messages.error(
            self.request,
                'Carrinho vazio.'
            )
            return redirect('produto:list')

        carrinho = self.request.session.get('carrinho')
        carrinho_varicao_ids = [v for v in carrinho]
        bd_variacaos = list(
            Variacao.objects.select_related('produto').filter(id__in=carrinho_varicao_ids)
        )
        
        for variacao in bd_variacaos:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativel'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativel_promocional'] = estoque * preco_unt_promo

                error_msg_estoque = 'Estoque insuficiente para alguns produtos do seu carrinho. \
                                     Reduzimos a quantidade desses produtos. Por favor, \
                                     verifique quais produtos forma afetados a seguir.'

            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque
                )
                self.request.session.save()
                return redirect('produto:cart')

        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_total_pagar(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )

        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id_'],
                    preco=v['preco_quantitativel'],
                    preco_promocinal=v['preco_quantitativel_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],

                ) for v in carrinho.values()
            ]
        )

        del self.request.session['carrinho']
        return redirect(
            reverse(
                'pedido:pay',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )
 


class Details(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/details.html'
    pk_url_kwarg = 'pk'
    

class List(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/list.html'
    paginate_by = 10
    ordering = ['-id']