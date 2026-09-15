# -*- coding: utf-8 -*-
"""Reescreve todo o <main> do index.html (hero + secoes) a partir de
produtos/catalogo.json. Rode da pasta produtos:  python3 gerar-site.py

Regra: produto sem url_afiliado nao entra no site."""
import io, json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'catalogo.json')
IDX  = os.path.join(BASE, 'index.html')

ROTULO = {'moda': 'MODA.', 'perfumaria': 'PERFUMARIA.', 'cotidiano': 'COTIDIANO.'}
CONTA  = {1:'Um', 2:'Dois', 3:'Tres', 4:'Quatro', 5:'Cinco', 6:'Seis', 7:'Sete',
          8:'Oito', 9:'Nove', 10:'Dez', 11:'Onze', 12:'Doze', 13:'Treze',
          14:'Quatorze', 15:'Quinze', 16:'Dezesseis', 17:'Dezessete',
          18:'Dezoito', 19:'Dezenove', 20:'Vinte'}
CONTA_ACENTO = {'Tres':'Três','Quatorze':'Catorze'}
SUBST  = {'moda': ('peca', 'pecas'), 'perfumaria': ('perfume', 'perfumes'),
          'cotidiano': ('objeto', 'objetos')}
ACENTO = {'peca':'peça', 'pecas':'peças'}

def numero(n):
    t = CONTA.get(n, str(n))
    return CONTA_ACENTO.get(t, t)

def foto(p):
    caminho = os.path.join(os.path.dirname(CAT), p.get('imagem', ''))
    if p.get('imagem') and os.path.exists(caminho):
        return 'produtos/' + p['imagem']
    return p.get('imagem_origem', '')

def cartao(p):
    src  = foto(p)
    href = p.get('url_afiliado') or p.get('url_produto') or '#'
    img  = ('<img class="cartao__img" src="%s" alt="%s" loading="lazy">' % (src, p['nome'])) if src else ''
    de   = ('\n          <p class="apoio cartao__de">%s</p>' % p['preco_de']) if p.get('preco_de') else ''
    raz  = ('\n          <p class="cartao__razao">%s</p>' % p['razao']) if p.get('razao') else ''
    return '''        <a class="cartao revelar" href="%s" target="_blank" rel="noopener sponsored nofollow">
          <div class="cartao__foto">%s</div>
          <h3 class="cartao__nome">%s</h3>
          <p class="apoio cartao__tecnica">%s</p>
          <p class="preco cartao__preco">%s</p>%s%s
        </a>''' % (href, img, p['nome'], p['tecnica'], p['preco'], de, raz)

def grupo(secao, itens):
    n = len(itens)
    sing, plur = SUBST[secao]
    palavra = sing if n == 1 else plur
    nota = '%s %s.' % (numero(n), ACENTO.get(palavra, palavra))
    return '''    <div class="secao__grupo" id="%s">

      <div class="selecao__cabecalho">
        <h2 class="t1 t1--versal">%s</h2>
        <p class="apoio">%s</p>
      </div>

      <div class="grade">

%s

      </div>
    </div>''' % (secao, ROTULO[secao], nota, '\n\n'.join(cartao(p) for p in itens))

def hero(cat, vivos):
    porid = dict((p['id'], p) for p in vivos)
    ids = [i for i in cat.get('vitrine', []) if i in porid] or [p['id'] for p in vivos[:5]]
    quadros, marcas = [], []
    for k, i in enumerate(ids):
        p = porid[i]
        quadros.append('''      <a class="vitrine__quadro%s" href="%s" target="_blank" rel="noopener sponsored nofollow"
         data-secao="%s" data-nome="%s" data-preco="%s" aria-label="%s, %s, abre na loja">
        <img class="vitrine__img" src="%s" alt="%s"%s>
      </a>''' % (' is-ativo' if k == 0 else '',
                 p.get('url_afiliado') or '#',
                 ROTULO[p['secao']], p['nome'], p['preco'], p['nome'], p['preco'],
                 foto(p), p['nome'], '' if k == 0 else ' loading="lazy"'))
        marcas.append('        <button class="vitrine__marca%s" type="button" aria-label="Ver %s"></button>'
                      % (' is-ativo' if k == 0 else '', p['nome']))
    primeiro = porid[ids[0]]
    return '''  <section class="hero" aria-labelledby="slogan">
    <div class="hero__texto">
      <p class="rotulo hero__rotulo">Moda &middot; Perfumaria &middot; Cotidiano</p>
      <h1 class="display" id="slogan">Presen&ccedil;a n&atilde;o<br>se explica.</h1>
      <div class="hero__acao">
        <a class="btn btn--primario" href="#selecao">Ver a sele&ccedil;&atilde;o</a>
        <span class="apoio">%s objetos. A compra acontece na loja de origem.</span>
      </div>
    </div>

    <div class="vitrine" id="vitrine">
%s
      <div class="vitrine__legenda">
        <p class="rotulo vitrine__secao">%s</p>
        <p class="vitrine__nome">%s</p>
        <p class="apoio vitrine__preco">%s</p>
      </div>
      <div class="vitrine__marcas">
%s
      </div>
    </div>
  </section>''' % (numero(len(vivos)), '\n'.join(quadros),
                   ROTULO[primeiro['secao']], primeiro['nome'], primeiro['preco'],
                   '\n'.join(marcas))

def main():
    cat   = json.load(io.open(CAT, encoding='utf-8'))
    html  = io.open(IDX, encoding='utf-8').read()
    vivos = [p for p in cat['produtos'] if p.get('url_afiliado')]
    fora  = [p['id'] for p in cat['produtos'] if not p.get('url_afiliado')]

    grupos = []
    for secao in cat['secoes']:
        itens = [p for p in vivos if p['secao'] == secao]
        if itens:
            grupos.append(grupo(secao, itens))

    selecao = ('''  <section class="secao faixa" id="selecao" aria-label="Sele&ccedil;&atilde;o">
    <div class="limite">

      <p class="apoio selecao__aviso">Cada objeto abre na loja onde ele &eacute; vendido.
      A ALTIVA ganha comiss&atilde;o por l&aacute;; voc&ecirc; paga o mesmo pre&ccedil;o.</p>

'''
        + '\n\n'.join(grupos) + '\n\n    </div>\n  </section>')

    novo = '<main>\n\n' + hero(cat, vivos) + '\n\n' + selecao + '\n\n</main>'
    ini = html.index('<main>')
    fim = html.index('</main>') + len('</main>')
    io.open(IDX, 'w', encoding='utf-8').write(html[:ini] + novo + html[fim:])

    print('index.html reescrito: %d produtos, vitrine com %d fotos'
          % (len(vivos), len([i for i in cat.get('vitrine', []) if any(p['id'] == i for p in vivos)])))
    if fora:
        print('fora (sem link comissionado): %s' % ', '.join(fora))

if __name__ == '__main__':
    main()
