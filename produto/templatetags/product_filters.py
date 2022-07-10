from django.template import Library
from utils import utils


register = Library()


@register.filter(name='formata_preco')
def formata_preco(val):
    return utils.formata_preco(val)
