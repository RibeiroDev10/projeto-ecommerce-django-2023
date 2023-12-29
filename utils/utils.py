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



def utils_cart_totals(carrinho):
    # Essa list_comprehension você faz de trás pra frente
    # Obtém o preco_quantitativo_promocional se estiver preenchido no carrinho (item.get('preco_quantitativo_promocional'))
    return sum(
        [
            item.get('preco_quantitativo_promocional')  # Se houver preço promocional, use esse
            if item.get('preco_quantitativo_promocional')  # Verifica se há preço promocional
            else item.get('preco_quantitativo')  # Caso contrário, use o preço regular
            for item in carrinho.values()  # Para cada item no carrinho
        ]
    )