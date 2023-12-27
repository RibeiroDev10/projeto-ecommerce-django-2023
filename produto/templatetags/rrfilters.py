from django.template import Library
from utils.utils import utils_formata_preco

register = Library()

@register.filter
def formata_preco(val):
    return utils_formata_preco(val)