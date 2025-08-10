# Dashboard Backend API

Backend robusto e escalável para sistema de dashboard, construído com FastAPI, SQLAlchemy e PostgreSQL.

## 🚀 Características

- **FastAPI**: Framework moderno e rápido para APIs
- **SQLAlchemy**: ORM robusto para banco de dados
- **Alembic**: Gerenciamento de migrações
- **PostgreSQL**: Banco de dados relacional
- **Pydantic**: Validação de dados
- **JWT**: Autenticação segura
- **CORS**: Suporte a requisições cross-origin
- **Documentação Automática**: Swagger UI e ReDoc

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL
- pip

## 🛠️ Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd backend
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Configure o banco de dados**
   - Crie um banco PostgreSQL
   - Atualize a URL do banco em `config.py` ou crie um arquivo `.env`

6. **Execute as migrações**
```bash
alembic upgrade head
```

## 🚀 Executando o Projeto

### Desenvolvimento
```bash
python main.py
```

### Produção
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

## 📁 Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── users.py
│   └── schemas/
│       ├── __init__.py
│       └── user.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── config.py
├── main.py
├── requirements.txt
├── alembic.ini
└── README.md
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do Banco de Dados
DATABASE_URL=postgresql://username:password@localhost:5432/dashboard_db

# Configurações da API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Configurações de Segurança
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configurações CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 📚 Endpoints da API

### Usuários

- `POST /api/v1/users/` - Criar usuário
- `GET /api/v1/users/` - Listar usuários
- `GET /api/v1/users/{user_id}` - Obter usuário específico
- `PUT /api/v1/users/{user_id}` - Atualizar usuário
- `DELETE /api/v1/users/{user_id}` - Remover usuário

### Sistema

- `GET /` - Endpoint raiz
- `GET /health` - Verificação de saúde
- `GET /docs` - Documentação Swagger
- `GET /redoc` - Documentação ReDoc

## 🔄 Migrações

### Criar nova migração
```bash
alembic revision --autogenerate -m "Descrição da migração"
```

### Aplicar migrações
```bash
alembic upgrade head
```

### Reverter migração
```bash
alembic downgrade -1
```

## 🧪 Testes

Para executar os testes (quando implementados):
```bash
pytest
```

## 📦 Deploy

### Docker (recomendado)
```bash
docker build -t dashboard-backend .
docker run -p 8000:8000 dashboard-backend
```

### Produção
1. Configure as variáveis de ambiente para produção
2. Use um servidor WSGI como Gunicorn
3. Configure um proxy reverso (Nginx)
4. Configure SSL/TLS

## 🔒 Segurança

- Senhas são hasheadas com bcrypt
- Validação de dados com Pydantic
- CORS configurado adequadamente
- JWT para autenticação
- Rate limiting (a ser implementado)

## 📈 Monitoramento

- Logs estruturados
- Métricas de performance
- Health checks
- Error tracking (a ser implementado)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para suporte, abra uma issue no repositório ou entre em contato com a equipe de desenvolvimento. 