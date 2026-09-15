# -*- coding: utf-8 -*-
"""Reescreve as secoes MODA, PERFUMARIA e COTIDIANO do index.html
a partir de produtos/catalogo.json. Rode da pasta produtos:  python3 gerar-site.py"""
import io, json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'catalogo.json')
IDX  = os.path.join(BASE, 'index.html')

ROTULO = {'moda': 'MODA.', 'perfumaria': 'PERFUMARIA.', 'cotidiano': 'COTIDIANO.'}
CONTA  = {1:'Um', 2:'Dois', 3:'Três', 4:'Quatro', 5:'Cinco', 6:'Seis',
          7:'Sete', 8:'Oito', 9:'Nove', 10:'Dez', 11:'Onze', 12:'Doze'}
SUBST  = {'moda': ('peça', 'peças'), 'perfumaria': ('perfume', 'perfumes'),
          'cotidiano': ('objeto', 'objetos')}

def cartao(p):
    # a imagem tratada mora em produtos/imagens; se ainda nao existe, usa a origem
    caminho = os.path.join(os.path.dirname(CAT), p.get('imagem', ''))
    src = 'produtos/' + p['imagem'] if p.get('imagem') and os.path.exists(caminho) else p.get('imagem_origem', '')
    href = p.get('url_afiliado') or p.get('url_produto') or '#'
    foto = ('<img class="cartao__img" src="%s" alt="%s" loading="lazy">' % (src, p['nome'])) if src else ''
    de = ('\n          <p class="apoio cartao__de">%s</p>' % p['preco_de']) if p.get('preco_de') else ''
    razao = ('\n          <p class="cartao__razao">%s</p>' % p['razao']) if p.get('razao') else ''
    return '''        <a class="cartao" href="%s" target="_blank" rel="noopener sponsored nofollow">
          <div class="cartao__foto">%s</div>
          <h3 class="cartao__nome">%s</h3>
          <p class="apoio cartao__tecnica">%s</p>
          <p class="preco cartao__preco">%s</p>%s%s
        </a>''' % (href, foto, p['nome'], p['tecnica'], p['preco'], de, razao)

def grupo(secao, itens):
    n = len(itens)
    sing, plur = SUBST[secao]
    nota = '%s %s.' % (CONTA.get(n, str(n)), sing if n == 1 else plur)
    cards = '\n\n'.join(cartao(p) for p in itens)
    return '''    <div class="secao__grupo" id="%s">

      <div class="selecao__cabecalho">
        <h2 class="t1 t1--versal">%s</h2>
        <p class="apoio">%s</p>
      </div>

      <div class="grade">

%s

      </div>
    </div>''' % (secao, ROTULO[secao], nota, cards)

def main():
    cat = json.load(io.open(CAT, encoding='utf-8'))
    html = io.open(IDX, encoding='utf-8').read()
    grupos = []
    # Regra ALTIVA: sem link comissionado, o produto nao entra no site.
    vivos = [p for p in cat['produtos'] if p.get('url_afiliado')]
    fora  = [p['id'] for p in cat['produtos'] if not p.get('url_afiliado')]
    for secao in cat['secoes']:
        itens = [p for p in vivos if p['secao'] == secao]
        if itens:
            grupos.append(grupo(secao, itens))
    novo = ('  <section class="secao faixa" id="selecao" aria-label="Seleção">\n'
            '    <div class="limite">\n\n' + '\n\n'.join(grupos) + '\n\n    </div>\n  </section>\n')
    ini = html.index('  <section class="secao faixa" id="selecao"')
    fim = html.index('</main>')
    io.open(IDX, 'w', encoding='utf-8').write(html[:ini] + novo + '\n' + html[fim:])
    print('index.html reescrito com %d produtos' % len(vivos))
    if fora:
        print('fora (sem link comissionado): %s' % ', '.join(fora))

if __name__ == '__main__':
    main()
