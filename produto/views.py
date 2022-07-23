from operator import mod
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q

from . import models
from perfil import models as models_perfil


class ListProducts(ListView):
    model = models.Produto
    template_name = 'produto/list.html'
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-id']


class ProductDetails(DetailView):
    model = models.Produto
    template_name = 'produto/detail.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:list')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não  existe'
            )
            return redirect(http_referer)
        
        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        variacao_id_ = variacao.id
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem_1

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(self.request, 'estoque insuficiente')
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            # variação existe no carrinho
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x '
                    f'no produto "{produto_nome}". Adicionamos {variacao_estoque}x no seu carrinho'
                )
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativel'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativel_promocional'] = preco_unitario_promocional * quantidade_carrinho

        else:
            # variação não existe no carrinho
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id_': variacao_id_,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,                
                'preco_quantitativel': preco_unitario,
                'preco_quantitativel_promocional': preco_unitario_promocional,
                'quantidade': quantidade,
                'slug': slug,
                'imagem': imagem,
            }
        
        self.request.session.save()

        messages.success(self.request, f'{produto_nome} {variacao_nome} adicionado ao seu carrinho')
        return redirect(http_referer)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:list')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        cart = self.request.session['carrinho'][variacao_id]

        messages.success(self.request, 
        f'Produto {cart["produto_nome"]} {cart["variacao_nome"]}'
        f' foi removido do seu carrinho.')
 
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)


class Cart(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
        }
        return render(self.request, 'produto/cart.html', contexto)


class Finish(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, 'Crie uma conta ou log para realizar sua compra')
            return redirect('perfil:create')

        perfil = models_perfil.Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.warning(
                self.request,
                'Usuário sem perfil'
            )
            return redirect('perfil:create')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Não há produtos para comprar.'
            )
            return redirect('produto:list')

        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
        }
        return render(self.request, 'produto/finish.html', contexto)


class Search(ListProducts):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)
        
        if not termo:
            return qs

        self.request.session['termo'] =  termo

        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )

        self.request.session.save()
        return qs
