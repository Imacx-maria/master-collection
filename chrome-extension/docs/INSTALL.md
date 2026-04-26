# Instalar a Master Collection Companion

Este guia é para instalar a extensão manualmente enquanto ainda não está publicada na Chrome Web Store.

## O Que Vais Instalar

**Master Collection Companion** é a extensão Chrome auxiliar para o Webflow Designer.

Ela funciona em:

```text
https://*.design.webflow.com/*
https://webflow.com/design/*
```

Funcionalidades atuais:

- Paste Guard para interceptar pastes de XscpData e detetar conflitos de classes.
- Ferramentas de limpeza de interações no Webflow Designer.
- UI compacta com tema automático light/dark e override manual.

## Instalação Local

1. Abre o Chrome.
2. Vai para:

```text
chrome://extensions
```

3. Liga **Developer mode** no canto superior direito.
4. Clica em **Load unpacked**.
5. Seleciona esta pasta:

```text
C:\Users\maria\Desktop\pessoal\FLOW_PARTY\MASTER-COLLECTION\chrome-extension
```

6. Confirma que aparece **Master Collection Companion** na lista de extensões.
7. Abre ou recarrega um projeto no Webflow Designer.
8. Clica no ícone da extensão na barra do Chrome.

## Uso Básico

### Paste Guard

1. Abre a extensão.
2. Entra no separador **Paste Guard**.
3. Liga o toggle.
4. Cola o payload no Webflow Designer normalmente.
5. Se houver conflitos de classes, a extensão mostra um aviso no browser.

### Interactions

1. Abre a extensão dentro de uma página do Webflow Designer.
2. Entra no separador **Interactions**.
3. Escolhe se queres ver todas, as da página atual, ou as unused.
4. Usa as ações com cuidado: apagar interações é destrutivo, embora possa ser possível desfazer com Ctrl+Z dentro do Designer.

## Tema

Por defeito, a UI segue o tema do sistema operativo/browser.

O botão no topo alterna entre:

- **System**
- **Light**
- **Dark**

A escolha fica guardada localmente no Chrome.

## Atualizar a Extensão Local

Depois de alterações ao código:

1. Vai a `chrome://extensions`.
2. Encontra **Master Collection Companion**.
3. Clica no botão de reload da extensão.
4. Recarrega também a tab do Webflow Designer.

## Resolver Problemas

### A extensão não aparece

- Confirma que selecionaste a pasta que contém `manifest.json`.
- Não seleciones uma pasta acima de `chrome-extension`.
- Confirma que `manifest.json` é JSON válido.

### O popup diz para abrir o Webflow Designer

- A extensão só injeta scripts em URLs do Webflow Designer.
- Abre uma página que corresponda a `https://*.design.webflow.com/*` ou `https://webflow.com/design/*`.

### O Paste Guard não reage

- Desliga e volta a ligar o toggle.
- Clica em reload na extensão em `chrome://extensions`.
- Recarrega a página do Webflow Designer.

### Erros depois de editar ficheiros

Abre `chrome://extensions`, lê o erro mostrado no cartão da extensão e corrige o ficheiro indicado.

