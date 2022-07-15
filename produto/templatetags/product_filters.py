from django.template import Library
from utils import utils


register = Library()


@register.filter(name='formata_preco')
def formata_preco(val):
    return utils.formata_preco(val)
    

@register.filter(name='cart_total_qtd')
def cart_total_qtd(carriho):
    return utils.cart_total_qtd(carriho)


@register.filter(name='cart_total')
def cart_total_pagar(carriho):
    return utils.cart_total_pagar(carriho)