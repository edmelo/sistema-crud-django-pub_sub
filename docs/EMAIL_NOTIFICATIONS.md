# Notificações por E-mail (Pub/Sub)

Este projeto utiliza um mecanismo de eventos (Publish/Subscribe) em `apps/core/pubsub.py`.
Os handlers de e-mail ficam inscritos via decorator `@event_handler` e utilizam o utilitário
central `apps/core/email.py` para envio.

## Eventos suportados

- Usuários
  - `USUARIO_CRIADO`: envia e-mail de boas-vindas para o usuário.
- Pedidos
  - `PEDIDO_CRIADO`: e-mail de confirmação do pedido ao usuário.
  - `PEDIDO_ENVIADO`: e-mail informando que o pedido foi enviado.
  - `PEDIDO_ENTREGUE`: e-mail de confirmação de entrega.
- Produtos
  - `PRODUTO_ESTOQUE_BAIXO`: e-mail para administradores.

Arquivos relevantes:

- `apps/core/email.py`: utilitário `send_system_email`.
- `apps/usuarios/signals.py`: handler de boas-vindas.
- `apps/pedidos/signals.py`: handlers de e-mail de pedido.
- `apps/produtos/signals.py`: handler de estoque baixo.

## Configuração de e-mail

- Desenvolvimento: backend de console
  - Configurado em `core/settings/development.py` com `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`.
  - Os e-mails não são enviados de verdade — são impressos no terminal.

- Produção: SMTP
  - `core/settings/production.py` lê as variáveis de ambiente:
    - `EMAIL_HOST`
    - `EMAIL_PORT` (padrão 587)
    - `EMAIL_USE_TLS` (True/False)
    - `EMAIL_HOST_USER`
    - `EMAIL_HOST_PASSWORD`
  - O remetente padrão (`DEFAULT_FROM_EMAIL`) é definido em `core/settings/base.py` e pode ser sobrescrito por `DEFAULT_FROM_EMAIL` ou, na ausência, cairá em `EMAIL_HOST_USER`.

Para notificar administradores no evento `PRODUTO_ESTOQUE_BAIXO` o sistema usa:

- `settings.ADMINS` (lista de tuplas `[("Nome", "email@exemplo")]`), se configurado; ou
- como fallback, `settings.EMAIL_HOST_USER`.

### Exemplo de variáveis de ambiente (SMTP)

```bash
EMAIL_HOST=smtp.seuprovedor.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=nao-responder@seudominio.com
EMAIL_HOST_PASSWORD=senha-super-secreta
DEFAULT_FROM_EMAIL=Seu Projeto <nao-responder@seudominio.com>
```

## Como testar rapidamente (dev)

Com o backend de console ativo, os e-mails aparecerão no terminal ao acionar eventos. Exemplos:

- Criar usuário pela interface/admin ou API aciona `USUARIO_CRIADO` (boas-vindas).
- Criar um `Pedido` aciona `PEDIDO_CRIADO` (confirmação).
- Atualizar `status` do pedido para `enviado` e depois `entregue` aciona os respectivos e-mails.
- Criar um `Produto` com `estoque < 5` aciona `PRODUTO_ESTOQUE_BAIXO` (requer `ADMINS` ou `EMAIL_HOST_USER` definido para haver destinatário).
