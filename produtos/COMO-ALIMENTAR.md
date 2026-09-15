# Como alimentar a ALTIVA

Fonte única: `catalogo.json`. O site é gerado dele. Nada é escrito à mão no index.html.

## Ordem obrigatória

1. **Link comissionado primeiro.** Sem `url_afiliado`, o produto não entra no site.
   O `gerar-site.py` ignora quem não tem link. Isso é regra, não preferência.
2. Foto revisada olho a olho (ver abaixo).
3. Só então entra no catálogo.

## Onde sair o link

- **Mercado Livre**: Gerador de links, `mercadolivre.com.br/afiliados/linkbuilder`.
  Aceita vários URLs, um por linha, e devolve `meli.la/...`. Etiqueta: `aljo8705981`.
- **Shopee**: botão "Obter link" no próprio cartão em
  `affiliate.shopee.com.br/offer/product_offer`, ou "Link personalizado" (até 5 por vez).
  Devolve `s.shopee.com.br/...`. O gerador tem teto diário: quando para de responder
  sem mensagem de erro, é cota, não bug. Espera e volta.
- A taxa de comissão fica visível no cartão da Shopee ("Taxa de comissão 16%") e no
  chip do hub do ML. Guardar no campo `comissao` do catálogo.

## Regra de foto (aprendida no erro)

Nenhum score automático decide foto. Monta a folha de contato da galeria inteira e
**olha**. Reprova na hora:

- mão, dedo, braço ou rosto cortado no quadro
- selo "100% ORIGINAL", "PREMIUM", badge de frete, moldura colorida
- texto sobreposto, infográfico, tabela de medidas, logo do vendedor
- fundo de campanha, colagem, recorte de cozinha na quina

Se o anúncio inteiro não tem uma foto limpa, troca de vendedor ou tira o produto.
A aba Ganhos Potencializados do ML é fonte legítima de comissão, mas a maioria dos
anúncios de lá é de vendedor commodity e reprova na foto. Pega a comissão onde ela
não custa a marca.

## Tratamento (padrão ALTIVA)

Todo cartão sai 1200x1600 (3:4), fundo Blanc, faixa de 190 px embaixo com filete Sand,
seção à esquerda e ALTIVA. à direita, Space Grotesk 500 com entreletra aberta.

Dois modos, e só dois:

- **A, silhueta.** Foto de fundo branco. Recorte por flood fill nas bordas, mantém só
  o maior componente conectado (isso derruba selo flutuante e prop solto), coloca sobre
  o Blanc com sombra suave. Cabe em 800x900 no centro alto do quadro.
- **B, cena.** Foto editorial (couro na madeira, vela no mármore, luminária na mesa).
  Corte cover para 1200x1410 e gradação quente leve para unificar com as outras.

O produto em si é sempre o pixel real do anúncio. IA entra no fundo e na cena, nunca
refazendo o produto: modelo de imagem devolve um sósia da peça de marca, o cliente
recebe outra coisa e a conta de afiliado paga.

## Transporte de imagem

Os CDNs (`http2.mlstatic.com`, `down-br.img.susercontent.com`) não são alcançáveis
fora do navegador, e o ML bloqueia hotlink em altiva.dpdns.org. Então: trata no
navegador, empacota tudo num ZIP só (o Chrome pergunta a pasta uma vez), descompacta
em `produtos/imagens/` e sobe os arquivos para o repositório. Imagem de produto no
site é sempre arquivo do repositório, nunca URL do marketplace.

## Limite dos marketplaces

Busca automatizada cansa em cerca de três consultas seguidas e passa a devolver página
vazia, sem erro. Alterna entre as duas lojas e espera. A API de afiliado da Shopee
(`/api/v3/offer/product/list`) aguenta muito mais que a interface e devolve nome, preço,
comissão e a galeria inteira de uma vez.

## Campos

```
id            moda-01, perfumaria-03, cotidiano-02
secao         moda | perfumaria | cotidiano
nome          curto, sem palavra-chave de vendedor
tecnica       material e medida, separados por ·
preco         "R$ 00,00"
preco_de      só quando existe âncora real
loja          mercadolivre | shopee
nota          média de avaliação
comissao      "16%" ou "ganhos extras"
url_produto   link cru, para conferência
url_afiliado  link comissionado. sem ele o produto não vai ao ar
imagem_origem URL da foto escolhida, para reprocessar depois
imagem        imagens/<id>.jpg
razao         uma frase do curador, aparece no cartão
```

## Publicar

```
cd produtos && python3 gerar-site.py
```
Depois subir `index.html`, `produtos/` e `assets/css/altiva.css` para
`github.com/jonallv/altiva` (branch main). O GitHub Pages publica em altiva.dpdns.org.
