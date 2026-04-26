# Publicar a Master Collection Companion na Chrome Web Store

Última verificação de fontes: 2026-04-25

Este documento lista o que falta preparar para transformar a extensão local numa extensão oficial da Chrome Web Store.

Fontes oficiais usadas:

- Chrome Web Store overview: https://developer.chrome.com/docs/webstore
- Register developer account: https://developer.chrome.com/docs/webstore/register
- Prepare your extension: https://developer.chrome.com/docs/webstore/prepare
- Publish in the Chrome Web Store: https://developer.chrome.com/docs/webstore/publish
- Fill out privacy fields: https://developer.chrome.com/docs/webstore/cws-dashboard-privacy
- Supplying images: https://developer.chrome.com/docs/webstore/images
- Listing requirements: https://developer.chrome.com/docs/webstore/program-policies/listing-requirements
- Developer Program Policies: https://developer.chrome.com/docs/webstore/program-policies/policies
- Distribution settings: https://developer.chrome.com/docs/webstore/cws-dashboard-distribution

## Estado Atual

Extensão:

```text
Master Collection Companion
```

Manifest:

```json
{
  "manifest_version": 3,
  "name": "Master Collection Companion",
  "version": "2.0.0",
  "permissions": ["activeTab", "scripting", "storage"],
  "host_permissions": [
    "https://*.design.webflow.com/*",
    "https://webflow.com/design/*"
  ]
}
```

Boa base:

- Já está em Manifest V3.
- As host permissions estão limitadas ao Webflow Designer.
- Não há backend nem login próprio.
- O armazenamento local atual parece limitado a preferências como Paste Guard e tema.

Antes de submeter:

- Rever se a versão inicial pública deve ser `0.1.0`, `1.0.0`, ou manter `2.0.0`.
- Substituir o ícone temporário `MC` por ícones finais da marca.
- Criar screenshots e imagem promocional.
- Escrever privacy policy pública.
- Testar em Chrome real com a extensão unpacked.

## Conta de Developer

1. Escolher uma conta Google para publicar.
2. Preferir um email dedicado à publicação, porque a Google indica que o email da conta de developer não é alterável depois da criação.
3. Aceder ao Chrome Web Store Developer Dashboard:

```text
https://chrome.google.com/webstore/devconsole
```

4. Aceitar o developer agreement e policies.
5. Pagar a taxa única de registo, se a conta ainda não estiver registada.

## Preparação Técnica

### Manifest

Confirmar antes do upload:

- `manifest_version` é `3`.
- `name` está final.
- `version` é superior a qualquer versão publicada antes.
- `description` tem no máximo 132 caracteres.
- `icons` aponta para imagens reais existentes.
- Não existem comentários no `manifest.json`.

Nota importante: depois do upload, metadata do manifest não é editável no dashboard. Se houver typo no manifest, é preciso alterar o ficheiro, incrementar versão e criar novo ZIP.

### ZIP Para Upload

O ZIP deve ter o `manifest.json` na raiz.

Não incluir:

- `.git/`
- docs internas
- ficheiros de desenvolvimento que não fazem parte da extensão
- screenshots brutas
- prompts ou handoffs

Incluir:

```text
manifest.json
content/
icons/
popup/
```

Comando sugerido a partir de `chrome-extension/`:

```powershell
Compress-Archive -Path manifest.json,content,icons,popup -DestinationPath .\dist\master-collection-companion.zip -Force
```

Antes de usar o comando, criar `dist/` se ainda não existir.

## Store Listing

A listing precisa de ser clara e não enganadora.

Campos a preparar:

- Nome: `Master Collection Companion`
- Short description: deve explicar a utilidade em uma frase curta.
- Detailed description: explicar Paste Guard e interaction tooling sem keyword stuffing.
- Categoria provável: Productivity ou Developer Tools.
- Idioma principal: inglês, a menos que o lançamento seja deliberadamente PT primeiro.
- Website/support URL: idealmente uma página no site Master Collection.

Draft curto possível:

```text
Master Collection Companion helps Webflow Designer users install and paste Master Collection packages more safely by detecting XscpData class conflicts and providing focused interaction utilities.
```

Evitar:

- prometer automação que a extensão não faz
- repetir "Webflow", "Chrome extension", "Master Collection" várias vezes para ranking
- screenshots ou descrições que mostrem features futuras

## Imagens Necessárias

Obrigatório:

- ícone de extensão 128x128 dentro do ZIP
- pelo menos 1 screenshot
- imagem promocional pequena 440x280

Recomendado:

- até 5 screenshots
- screenshot em 1280x800 quando possível
- imagem promocional marquee 1400x560 se quisermos hipótese de destaque

Requisitos/práticas importantes:

- screenshots devem mostrar a experiência real da extensão
- screenshots devem ter cantos quadrados e sem padding
- screenshots aceites: 1280x800 ou 640x400
- promo image pequena: 440x280
- promo image marquee opcional: 1400x560
- evitar texto excessivo nas imagens promocionais

TODO atual:

- trocar os ícones temporários `MC` por assets finais.
- gerar screenshots do popup em light e dark.
- gerar screenshot do aviso Paste Guard no Webflow Designer.
- criar imagem promocional 440x280 com a marca final.

## Privacy Tab

A Google pede:

- single purpose claro e estreito
- justificação para cada permission
- declaração de uso de dados
- privacy policy URL
- declaração sobre remote code

### Single Purpose Sugerido

```text
Help Webflow Designer users paste Master Collection packages safely by detecting XscpData class conflicts and providing focused interaction cleanup tools on Webflow Designer pages.
```

### Permissions Atuais e Justificação

`activeTab`

```text
Used to communicate with the active Webflow Designer tab only when the user opens the extension popup.
```

`scripting`

```text
Used to inject the companion content scripts into the active Webflow Designer tab when Chrome has not already loaded them.
```

`storage`

```text
Used to store local extension preferences, such as Paste Guard enabled state and popup theme preference.
```

Host permissions:

```text
https://*.design.webflow.com/*
https://webflow.com/design/*
```

Justificação:

```text
Required so the extension can run only inside Webflow Designer, where Paste Guard and interaction cleanup features operate.
```

### User Data Assessment Atual

Com base no código atual, a extensão:

- lê a DOM do Webflow Designer para detetar interações/classes
- guarda preferências locais no `chrome.storage.local`
- não envia dados para servidores externos
- não tem analytics
- não tem login
- não usa Google APIs
- não executa remote code

Isto deve ser revisto antes da submissão final com uma leitura completa do código.

### Privacy Policy

Mesmo que a extensão não envie dados para fora do browser, preparar uma privacy policy pública.

Deve dizer:

- que dados são processados localmente
- que preferências são guardadas localmente
- que não há venda de dados
- que não há transferência para terceiros
- que não há analytics se isso continuar verdadeiro
- contacto de suporte

Se algum dia usar Google APIs ou recolher user data, a policy deve incluir uma declaração de conformidade com a Chrome Web Store User Data Policy e Limited Use requirements.

## Distribution

Opções da Google:

- **Public**: listada publicamente na Chrome Web Store.
- **Unlisted**: instalável por link, não aparece na pesquisa pública.
- **Private**: só trusted testers, grupos ou domínio quando aplicável.

Recomendação:

1. Primeiro publicar como **Private** para trusted testers.
2. Depois usar **Unlisted** para clientes/testers externos controlados.
3. Só passar para **Public** quando a listing, suporte, assets e privacy estiverem estáveis.

## Test Instructions Para Review

Se necessário, fornecer instruções para o reviewer:

```text
1. Open a Webflow Designer project at https://webflow.com/design/... or https://*.design.webflow.com/...
2. Open the Master Collection Companion popup.
3. Enable Paste Guard.
4. Paste an XscpData payload into the Webflow Designer canvas.
5. Use the Interactions tab to scan available Webflow interactions on the current Designer page.

No account inside the extension is required. The extension only runs on Webflow Designer pages.
```

Se o reviewer precisar de uma conta Webflow ou projeto de teste, preparar antes:

- email de teste
- password temporária
- URL de projeto Webflow de teste
- payload XscpData seguro para testar conflitos

Não pôr credenciais reais em ficheiros do repo.

## Submission Flow

1. Testar extensão localmente em Chrome.
2. Rever manifest.
3. Criar ZIP com `manifest.json` na raiz.
4. Entrar no Developer Dashboard.
5. Add new item.
6. Fazer upload do ZIP.
7. Preencher Store Listing.
8. Preencher Privacy tab.
9. Preencher Distribution.
10. Adicionar Test instructions se necessário.
11. Submeter para review.
12. Usar deferred publishing se quisermos controlar o momento em que passa a live.

## Checklist Final Antes de Submeter

- [ ] Nome final aprovado.
- [ ] Ícone final 128x128 no ZIP.
- [ ] Ícones 16/48/128 finais no manifest.
- [ ] Description com <= 132 caracteres.
- [ ] Sem permissões desnecessárias.
- [ ] Sem remote code.
- [ ] Sem analytics não documentado.
- [ ] Sem logs ruidosos ou debug desnecessário.
- [ ] Privacy policy pública criada.
- [ ] Store listing completa.
- [ ] Screenshot obrigatório criado.
- [ ] Promo image 440x280 criada.
- [ ] Testado em Chrome com `Load unpacked`.
- [ ] Testado em pelo menos um projeto Webflow Designer real.
- [ ] ZIP criado com `manifest.json` na raiz.
- [ ] Test instructions preparadas se houver login/projeto de teste.

## Riscos Atuais

1. **Ícone temporário**

O ícone `MC` serve para desenvolvimento, mas não deve ser o asset final da Store.

2. **Interaction delete é sensível**

Como apagar interações pode ser destrutivo, a descrição e a UI devem ser cuidadosas. A feature deve deixar claro o escopo e o risco.

3. **Dependência do DOM do Webflow**

Se o Webflow alterar o Designer DOM, a extensão pode partir. A listing não deve prometer compatibilidade absoluta.

4. **Webflow trademark**

Usar "Webflow" apenas de forma descritiva. Evitar parecer extensão oficial da Webflow.

