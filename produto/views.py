from operator import mod
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from . import models


class ListProducts(ListView):
    model = models.Produto
    template_name = 'produto/list.html'
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['id']


class ProductDetails(DetailView):
    model = models.Produto
    template_name = 'produto/detail.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'
 

class AddToCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AddToCart')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoveFromCart')


class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')


class Finish(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finish')
