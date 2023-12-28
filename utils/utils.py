from pprint import pprint
from var_dump import var_dump

def utils_formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')



def utils_cart_total_qtd(carrinho):
    # carrinho.values() --> Retorna os índice das Variações do carrinho sendo acessível no for abaixo.
    # for item in carrinho.values() --> Percorre e acessa os índices das variações do carrinho, deixando acessível os atributos do produto daquele índice de variação
    # item['quantidade'] --> Acessa o atributo 'quantidade' do Produto, com base na variação percorrida acima.
    soma_qtd_produtos_por_variacao = sum([item['quantidade'] for item in carrinho.values()])
    return soma_qtd_produtos_por_variacao