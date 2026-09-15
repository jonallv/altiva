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


# ---------------------------------------------------------------- redirecionadores
# Regra da marca: todo post carrega link de afiliado, e o link precisa ser curto,
# digitavel e clicavel. Cada produto ganha altiva.dpdns.org/r/<slug>, que manda
# direto para a loja. Se o anuncio cair, muda-se o destino aqui e o post continua valendo.

REDIR = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>%(nome)s &middot; ALTIVA.</title>
<meta http-equiv="refresh" content="0; url=%(link)s">
<link rel="canonical" href="%(link)s">
<link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../../assets/css/altiva.css">
<style>
  body{min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center}
  .ponte{padding:var(--margem)}
  .ponte__marca{font-family:var(--grotesk);font-weight:500;font-size:28px;letter-spacing:.2em;color:var(--titulo)}
  .ponte__rule{width:120px;height:1px;background:var(--linha);margin:var(--e4) auto}
</style>
</head>
<body class="noir">
  <div class="ponte">
    <p class="ponte__marca">ALTIVA.</p>
    <div class="ponte__rule"></div>
    <p class="corpo">%(nome)s</p>
    <p class="apoio mt-2">Levando voc&ecirc; at&eacute; a %(loja)s&hellip;</p>
    <p class="mt-4"><a class="btn btn--primario" href="%(link)s" rel="noopener sponsored nofollow">Abrir agora</a></p>
    <p class="apoio mt-4">Link de afiliado. Voc&ecirc; paga o mesmo pre&ccedil;o.</p>
  </div>
<script>location.replace("%(link)s");</script>
</body>
</html>
"""

HUB_LINHA = """      <a class="atalho" href="%(link)s" target="_blank" rel="noopener sponsored nofollow">
        <span class="atalho__nome">%(nome)s</span>
        <span class="atalho__meta">%(tecnica)s</span>
        <span class="atalho__preco">%(preco)s</span>
      </a>"""

HUB = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>A sele&ccedil;&atilde;o &middot; ALTIVA.</title>
<meta name="description" content="Todos os objetos da sele&ccedil;&atilde;o ALTIVA, cada um abrindo direto na loja.">
<meta name="theme-color" content="#0B0B0C">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../assets/css/altiva.css">
<style>
  .hub{max-width:560px;margin:0 auto;padding:var(--e6) var(--margem) var(--e7)}
  .hub__marca{font-family:var(--grotesk);font-weight:500;font-size:26px;letter-spacing:.2em;color:var(--titulo);display:block;text-align:center}
  .hub__linha{width:120px;height:1px;background:var(--linha);margin:var(--e3) auto var(--e5)}
  .hub__secao{margin-top:var(--e5)}
  .atalho{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px var(--e3);
    padding:var(--e3) 0;border-bottom:1px solid var(--linha);text-decoration:none;
    transition:opacity var(--transicao)}
  .atalho:hover{opacity:.62}
  .atalho__nome{font-family:var(--grotesk);font-weight:500;font-size:17px;color:var(--titulo)}
  .atalho__preco{font-family:var(--sans);font-weight:400;font-size:15px;color:var(--titulo);text-align:right;align-self:center;grid-row:span 2}
  .atalho__meta{font-family:var(--sans);font-weight:300;font-size:13px;color:var(--apoio)}
</style>
</head>
<body class="noir">
<main class="hub">
  <a class="hub__marca" href="../index.html">ALTIVA.</a>
  <div class="hub__linha"></div>
  <p class="apoio" style="text-align:center">Cada objeto abre direto na loja.<br>Link de afiliado: voc&ecirc; paga o mesmo pre&ccedil;o.</p>
%(secoes)s
  <p class="mt-6" style="text-align:center"><a class="link" href="../index.html">Ver a boutique</a></p>
</main>
</body>
</html>
"""

# O GitHub Pages nao cria diretorio bonito sem Jekyll, entao quem resolve
# /r/<slug> e o 404.html: ele le o caminho, acha o slug no mapa e redireciona.
# Um arquivo so, URL limpa, e slug errado cai no hub em vez de dar erro.
ROTEADOR = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>ALTIVA.</title>
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/altiva.css">
<style>
  body{min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center}
  .ponte{padding:var(--margem);max-width:420px}
  .ponte__marca{font-family:var(--grotesk);font-weight:500;font-size:28px;letter-spacing:.2em;color:var(--titulo)}
  .ponte__rule{width:120px;height:1px;background:var(--linha);margin:var(--e4) auto}
</style>
<script>
(function(){
  var mapa = %(mapa)s;
  var p = location.pathname.replace(/\/+$/,'').split('/');
  if (p.length >= 3 && p[p.length-2] === 'r') {
    var alvo = mapa[p[p.length-1].toLowerCase()];
    if (alvo) { location.replace(alvo); return; }
    location.replace('/r/'); return;
  }
  if (p[p.length-1] === 'r') { location.replace('/r/'); return; }
  window.__perdido = true;
})();
</script>
</head>
<body class="noir">
  <div class="ponte">
    <p class="ponte__marca">ALTIVA.</p>
    <div class="ponte__rule"></div>
    <p class="corpo" id="recado">Levando voc&ecirc; at&eacute; a loja&hellip;</p>
    <p class="mt-4"><a class="btn btn--primario" href="/r/">Ver a sele&ccedil;&atilde;o</a></p>
    <p class="apoio mt-4">Links de compra s&atilde;o de afiliado. Voc&ecirc; paga o mesmo pre&ccedil;o.</p>
  </div>
<script>
if (window.__perdido) document.getElementById('recado').textContent = 'Esta p\u00e1gina n\u00e3o existe.';
</script>
</body>
</html>
"""

def redirecionadores(cat, vivos):
    raiz = os.path.join(BASE, 'r')
    if not os.path.isdir(raiz):
        os.makedirs(raiz)
    for p in vivos:
        slug = p.get('slug') or p['id']
        pasta = os.path.join(raiz, slug)
        if not os.path.isdir(pasta):
            os.makedirs(pasta)
        io.open(os.path.join(pasta, 'index.html'), 'w', encoding='utf-8').write(
            REDIR % {'nome': p['nome'], 'link': p['url_afiliado'],
                     'loja': 'Shopee' if p['loja'] == 'shopee' else 'Mercado Livre'})
    partes = []
    for secao in cat['secoes']:
        itens = [p for p in vivos if p['secao'] == secao]
        if not itens:
            continue
        linhas = '\n'.join(HUB_LINHA % {'link': p['url_afiliado'], 'nome': p['nome'],
                                        'tecnica': p['tecnica'], 'preco': p['preco']} for p in itens)
        partes.append('  <section class="hub__secao">\n    <p class="rotulo">%s</p>\n%s\n  </section>'
                      % (ROTULO[secao], linhas))
    io.open(os.path.join(raiz, 'index.html'), 'w', encoding='utf-8').write(HUB % {'secoes': '\n'.join(partes)})
    mapa = json.dumps(dict((p.get('slug') or p['id'], p['url_afiliado']) for p in vivos),
                      ensure_ascii=False, indent=2)
    io.open(os.path.join(BASE, '404.html'), 'w', encoding='utf-8').write(ROTEADOR % {'mapa': mapa})
    return len(vivos)


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

    n = redirecionadores(cat, vivos)
    print('r/ gerado: %d redirecionadores + hub' % n)
    print('index.html reescrito: %d produtos, vitrine com %d fotos'
          % (len(vivos), len([i for i in cat.get('vitrine', []) if any(p['id'] == i for p in vivos)])))
    if fora:
        print('fora (sem link comissionado): %s' % ', '.join(fora))

if __name__ == '__main__':
    main()
