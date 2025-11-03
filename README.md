# Sistema CRUD Django

Sistema completo de gerenciamento com arquitetura MVC/MVT, operações CRUD, microsserviços e deploy AWS.

## 👥 Equipe de Desenvolvimento

- **Ednaldo Batista de Melo** - Backend/Infraestrutura
- **Carolline Dias Pena** - Full-Stack/AWS

## 🚀 Tecnologias Utilizadas

- **Backend:** Python 3.11, Django 4.2.7
- **API:** Django REST Framework 3.14.0
- **Banco de Dados:** SQLite (otimizado para produção)
- **Frontend:** Bootstrap 5, HTML5, JavaScript
- **Containerização:** Docker & Docker Compose
- **Cloud:** AWS (EC2, Lambda, S3)
- **Versionamento:** Git & GitHub

## 🏗️ Arquitetura

# Sistema CRUD Django

Projeto Django com CRUD para Usuários, Produtos e Pedidos, empacotado com Docker para desenvolvimento e testes.

Este README foi atualizado para detalhar o fluxo com Docker (volumes, static files e nginx) — veja a seção "Docker" abaixo.

## Tecnologias

- Python 3.11
- Django 4.x
- Django REST Framework
- Docker & Docker Compose

## Como usar (rápido)

1) Subir ambiente com Docker (recomendado):

```bash
docker-compose up -d --build
```

2) Ver logs:

```bash
docker-compose logs -f web
docker-compose logs -f nginx
```

3) Acesse a aplicação:

- Aplicação: http://localhost/
- Admin: http://localhost:8000/admin/

## Detalhes sobre Docker e static files

Arquitetura do Docker usada aqui (resumido):

- Serviço `web`: roda Gunicorn (após `entrypoint.sh` que executa `migrate` e `collectstatic`).
- Serviço `nginx`: serve `/static/` e `/media/` a partir de volumes, e faz proxy para `web`.
- Volumes nomeados usados:
  - `static_volume` → montado em `/app/staticfiles` (STATIC_ROOT)
  - `media_volume` → montado em `/app/media`

Por que isso importa: o `collectstatic` precisa gravar em um local que o `nginx` consiga ler. Para isso usamos um volume nomeado compartilhado (`static_volume`). O `entrypoint.sh` do `web` roda `collectstatic` em runtime e popula esse volume.

Comandos úteis:

- Rodar collectstatic manualmente:
  ```bash
  docker-compose run --rm web python manage.py collectstatic --noinput --settings=core.settings.development
  ```
- Verificar arquivo estático servido pelo nginx:
  ```bash
  curl -I http://localhost/static/css/style.css
  ```

## Configuração do nginx (local)

- Arquivo de configuração local: `nginx.conf/default.conf` (montado em `/etc/nginx/conf.d` no container)
- Observação: se você encontrar um problema de montagem onde o Docker reclama de "Are you trying to mount a directory onto a file (or vice-versa)?", verifique se `./nginx.conf` é um diretório contendo `default.conf`. No repositório corrigimos esse caso criando `nginx.conf/default.conf`.

Se for necessário remover uma entrada problemática criada por engano (por exemplo um diretório `nginx.conf/default.conf/` criado com dono root), execute localmente:

```bash
sudo rm -rf ./nginx.conf/default.conf
mkdir -p ./nginx.conf
# criar o arquivo ./nginx.conf/default.conf com o conteúdo apropriado
```

## Troubleshooting rápido

- Se `nginx` reclama que não consegue modificar `/etc/nginx/conf.d/default.conf` ao iniciar, isso geralmente acontece porque montamos o diretório como read-only; é um aviso do entrypoint, não necessariamente falha. O nginx normalmente carrega a configuração mesmo assim.
- Se arquivos estáticos não aparecem, verifique:
  - `docker-compose logs web` — o `collectstatic` deve rodar no startup
  - `docker-compose exec nginx ls -l /app/staticfiles` — confirme os arquivos presentes

## Desenvolvimento local sem Docker

Siga os passos clássicos do Django:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Observações finais

- O `entrypoint.sh` executa `migrate` e `collectstatic` antes de iniciar o Gunicorn — isso facilita desenvolvimento com volumes montados.
- Para produção, prefira um fluxo de deploy que rode `collectstatic` como um job separado e use um sistema de armazenamento estático dedicado (S3, CDN).


