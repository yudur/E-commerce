def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')


def cart_total_qtd(carriho):
    return sum([item['quantidade'] for item in carriho.values()])


def cart_total_pagar(carriho):
    total = 0
    for item in carriho.values():
        if item['preco_quantitativel_promocional']:
            total += item['preco_quantitativel_promocional']
        else:
            total += item['preco_quantitativel']

    return total
