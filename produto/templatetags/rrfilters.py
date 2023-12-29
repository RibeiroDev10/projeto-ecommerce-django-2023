from django.template import Library
from utils.utils import utils_formata_preco, utils_cart_total_qtd, utils_cart_totals

register = Library()

@register.filter
def formata_preco(val):
    return utils_formata_preco(val)

@register.filter
def cart_total_qtd(carrinho):
    return utils_cart_total_qtd(carrinho)

@register.filter
def cart_totals(carrinho):
    return utils_cart_totals(carrinho)