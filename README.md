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

O sistema segue o padrão **MTV (Model-Template-View)** do Django com:

- **3 Apps principais:**
  - `usuarios` - Gerenciamento de usuários e autenticação
  - `produtos` - Catálogo e controle de estoque
  - `pedidos` - Sistema de pedidos com processamento assíncrono

- **Componentes especiais:**
  - Sistema **Publish-Subscribe** para eventos
  - **Microsserviços** REST API
  - **Processamento Serverless** com AWS Lambda

## 📋 Funcionalidades

### ✅ Operações CRUD
- **Create** - Criação de registros
- **Read** - Consulta e listagem
- **Update** - Edição de dados
- **Delete** - Remoção (soft delete)

### ✅ Sistema de Usuários
- Autenticação e autorização
- Perfis personalizáveis
- Validação de CPF e telefone
- Sistema de tokens (API)

### ✅ Gestão de Produtos
- Controle de estoque
- Categorização
- Busca e filtros
- API REST completa

### ✅ Sistema de Pedidos
- Processamento assíncrono
- Integração com produtos
- Status tracking
- Notificações via Pub/Sub

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- pip
- Git
- Docker (opcional)

### Instalação Local

1. **Extraia o projeto:**
```bash
unzip sistema_crud_completo.zip
cd sistema_crud
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements/development.txt
```

4. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

5. **Execute as migrações:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crie um superusuário:**
```bash
python manage.py createsuperuser
```

7. **Execute o servidor de desenvolvimento:**
```bash
python manage.py runserver
```

### Instalação com Docker

1. **Extraia o projeto:**
```bash
unzip sistema_crud_completo.zip
cd sistema_crud
```

2. **Execute com Docker Compose:**
```bash
docker-compose up --build
```

## 🌐 URLs Principais

- **Home:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/
- **API Usuários:** http://localhost:8000/api/usuarios/
- **API Produtos:** http://localhost:8000/api/produtos/
- **API Pedidos:** http://localhost:8000/api/pedidos/

## 📁 Estrutura do Projeto

```
sistema_crud/
├── apps/
│   ├── core/           # Funcionalidades compartilhadas
│   ├── usuarios/       # App de usuários (Ednaldo)
│   ├── produtos/       # App de produtos (Carolline)
│   └── pedidos/        # App de pedidos (Carolline)
├── core/
│   ├── settings/       # Configurações por ambiente
│   ├── urls.py         # URLs principais
│   ├── wsgi.py         # WSGI para produção
│   └── asgi.py         # ASGI para funcionalidades assíncronas
├── templates/          # Templates HTML
├── static/             # Arquivos estáticos
├── requirements/       # Dependências por ambiente
├── docker-compose.yml  # Configuração Docker
├── Dockerfile          # Imagem Docker
├── manage.py           # Comando Django
└── README.md           # Este arquivo
```

## 📝 Requisitos Atendidos

- ✅ **Arquitetura MVC** - Sistema frontend + backend
- ✅ **Operações CRUD** - Create, Read, Update, Delete
- ✅ **3 Entidades** - Usuários, Produtos, Pedidos
- ✅ **Banco de Dados** - SQLite otimizado
- ✅ **Histórico Git** - Commits estruturados
- ✅ **Microsserviços** - API REST completa
- ✅ **Publish-Subscribe** - Sistema de eventos
- ✅ **Serverless** - AWS Lambda
- ✅ **Deploy AWS** - EC2/Lambda configurado

## 📞 Suporte

Para dúvidas ou problemas:

- **Ednaldo Batista de Melo** - Backend/Infraestrutura
- **Carolline Dias Pena** - Full-Stack/AWS

## 📄 Licença

Este projeto é desenvolvido para fins acadêmicos.

---

**Desenvolvido com ❤️ para a disciplina de Desenvolvimento Web**
