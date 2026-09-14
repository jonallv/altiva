# ALTIVA.

Boutique digital de curadoria em moda e perfumaria. Site estático, sem build e sem
dependências. Construído a partir do Manual da Marca ALTIVA, versão 1.0.

## Arquivos

```
index.html          Home: hero, coleção de doze objetos, rodapé
produto.html        Página de produto (PDP): foto fixa, texto rolável
curador.html        Manifesto e políticas, na superfície Noir
assets/css/altiva.css   Sistema de interface: tokens, tipografia, componentes
assets/favicon.svg  Monograma "A." em Bone sobre Noir
.nojekyll           Evita o processamento Jekyll no GitHub Pages
```

## Sistema

Sete cores, nenhuma outra: Noir #0B0B0C, Bone #F3F0EA, Blanc #FFFFFF,
Graphite #2A2A2D, Stone #6E6961, Sand #D8D1C6, Âmbar #A67052.

Duas fontes, ambas do Google Fonts: Space Grotesk (400, 500) para logotipo,
títulos e rótulos; DM Sans (300, 400, 500) para parágrafos, interface e preços.
Nenhum peso acima de 500.

Grid de base 8. Margens de 48 px no desktop e 20 px no mobile. Calha de 24 px e
16 px. Entre seções: 128 px e 80 px.

Um só modo de cor. O fundo padrão é Bone. A classe `.noir` no `body` troca a
superfície para campanha. Não existe toggle de modo escuro.

## Como publicar

**GitHub Pages.** Suba a pasta para um repositório, abra Settings, Pages e
aponte a origem para a branch principal, pasta raiz. O `.nojekyll` já está
incluído.

**Vercel.** Importe o repositório, framework "Other", sem comando de build,
diretório de saída igual à raiz.

## Ao editar

Antes de publicar qualquer alteração, rode o checklist do capítulo 09 do manual:
produto como elemento mais visível, apenas as sete cores, Âmbar abaixo de 5%,
nenhum Bold em título, logotipo com ponto e tracking de +12% em uma única
ocorrência por superfície, nenhuma exclamação, emoji, hashtag ou palavra
proibida, frases de até 12 palavras com ponto final.
