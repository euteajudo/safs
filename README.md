# Documentação SAFS – Backend e Frontend

## Sumário
- [Arquitetura Geral](#arquitetura-geral)
- [Backend (FastAPI)](#backend-fastapi)
  - [Autenticação e Segurança](#autenticação-e-segurança)
  - [Rotas Principais](#rotas-principais)
  - [Modelos / Schemas](#modelos--schemas)
  - [Dependências e Stack](#dependências-e-stack)
- [Frontend (Next.js 15)](#frontend-nextjs-15)
  - [Fluxo de Autenticação](#fluxo-de-autenticação)
  - [Telas](#telas)
  - [Integração com API](#integração-com-api)
  - [Dependências e Stack](#dependências-e-stack-1)
- [Observações e Recomendações](#observações-e-recomendações)

---

## Arquitetura Geral
- **Backend:** FastAPI assíncrono, PostgreSQL via SQLAlchemy async, autenticação JWT, documentação Swagger/ReDoc.
- **Frontend:** Next.js 15 (App Router) + React 19 + TypeScript; UI com shadcn/Radix/Tailwind v4; tabelas com TanStack; gráficos Recharts.
- **Proxy:** `/api/backend` no frontend faz rewrite para `http://192.168.0.32:8000/api/:path*` (configurado em `next.config.ts`).
- **Middleware de auth:** rota `/dashboard` exige cookie `token`; `/login` redireciona para dashboard se já autenticado.

---

## Backend (FastAPI)
**Base:** `http://<host>:8000/api/v1`

### Autenticação e Segurança
- `POST /token` (OAuth2 password) → `{ access_token, token_type, user }`.
- JWT HS256 (`SECRET_KEY`), expiração padrão 60 min.
- Senhas com bcrypt (passlib).
- Dependência `get_current_active_user` protege rotas marcadas.
- CORS liberado (`*`) para desenvolvimento; restringir em produção.

### Rotas Principais
- **Health/Teste**
  - `GET /health`: status.
  - `GET /test-auth`: público de teste.
  - `POST /login-simple`: login simplificado (username/password) → token.

- **Login**
  - `POST /token`: autenticação principal (form `username`, `password`).

- **Usuários** (`/users`)
  - `GET /stats` (auth): totais/ativos/novos 30d.
  - `POST /`: cria usuário (unidade, nome, username, email, senha, flags de permissão).
  - `GET /`: lista paginada (`skip`, `limit`).
  - `GET /me` (auth): dados do logado.
  - `GET /{user_id}`: busca por ID.
  - `PATCH /{user_id}` (auth): self ou superuser.
  - `DELETE /{user_id}` (auth): só superuser/chefes; 204.
  - `GET /unidade/{unidade}`: lista por unidade (hoje retorna `None` por bug de retorno).

- **Catálogo de Itens** (`/catalogo`, auth)
  - `GET /stats`: totais, por classificação XYZ, novos 30d.
  - `POST /`: cria item (`unidade`, `codigo_master`, `descritivo_resumido`, campos opcionais AGHU/CATMAT/EBSERH, `classificacao_xyz`, `observacao`, relacionamentos 1:N e N:N).
  - `GET /`: lista (`skip`, `limit`).
  - `GET /{item_id}`; `GET /codigo_master/{codigo_master}`; `GET /check-codigo-master/{codigo_master}`.
  - `PATCH /{item_id}`: atualização parcial.
  - `DELETE /{item_id}`: só superuser/chefe_unidade/chefe_setor (204).
  - N:N: `POST /{item_id}/compradores`, `POST /{item_id}/controladores`; `GET` equivalentes listam.

- **Processos de Aquisição** (`/processos`, auth)
  - `GET /stats`: totais, por status, novos 30d.
  - `POST /`: cria processo (número de planejamento, item, status, `comprador_ids`).
  - `GET /`: lista (`skip`, `limit`).
  - `GET /{processo_id}`; `GET /numero/{numero_processo}`.
  - `PATCH /{processo_id}`: atualização parcial.
  - `DELETE /{processo_id}`: só superuser (204).
  - `GET /unidade/{unidade}`: lista por unidade.
  - N:N compradores: `POST /{processo_id}/compradores`; `GET /{processo_id}/compradores`; `GET /comprador/{comprador_id}`.

- **Responsáveis Técnicos** (`/responsaveis-tecnicos`, auth)
  - `POST /`, `GET /`, `GET /{id}`, `GET /nome/{nome}`, `PATCH /{id}`, `DELETE /{id}` (delete só superuser/chefes).

### Modelos / Schemas
- **User:** unidade, nome, username, email, foto_url?, flags (`is_active`, `is_superuser`, `is_chefe_unidade`, `is_chefe_setor`, `is_funcionario`), timestamps.
- **ItemCatalogo:** campos de identificação/códigos (AGHU, CATMAT, EBSERH), `classificacao_xyz`, `apresentacao`, `observacao`, relacionamentos 1:N (`comprador_id`, `controlador_id`) e N:N (`processo_ids`, `comprador_ids`, `controlador_ids`).
- **Processo:** unidade, `objeto_aquisicao`, `numero_processo_planejamento`, `numero_item`, `codigo_master`, status enums, `observacao`, `comprador_ids`.
- **ResponsavelTecnico:** `nome_res_tec`.
- **Token:** `access_token`, `token_type`, `user` (metadados do usuário).

### Dependências e Stack
- FastAPI, SQLAlchemy async, Alembic, PostgreSQL (asyncpg), Pydantic v2, JWT (python-jose), passlib[bcrypt], python-multipart, uvicorn, python-dotenv.

---

## Frontend (Next.js 15)

### Fluxo de Autenticação
- `LoginForm` chama `loginApi` → `POST /api/backend/v1/token` (form data).
- Salva JWT em `localStorage` + cookie `token`; `AuthProvider` restaura usuário; `useCurrentUser` expõe contexto.
- `middleware.ts`: se acessar `/dashboard` sem cookie → `/login`; se `/login` com cookie → `/dashboard`.

### Telas
- `/` → redireciona para `/dashboard`.
- `/login`: formulário de login com loader, erro e toggle de senha.
- `/dashboard` (home): sidebar, header, cards, gráfico, tabela mock `data.json`.
- `/dashboard/catalogo`: fetch real `GET /v1/catalogo/`; tabela com filtros, seleção em massa, delete (`DELETE /v1/catalogo/{id}`), criação/edição via `CatalogoFormDialog`, exporta Excel.
- `/dashboard/processos`: cards + gráfico + tabela mock `data-processos.json`.
- `/dashboard/empenhos`: cards + gráfico + tabela mock `data.json`.
- `/dashboard/usuarios`: fetch real `GET /v1/users/`; filtros por unidade/status/perfis; criar/editar via `UsuarioFormDialog`; delete em massa `DELETE /v1/users/{id}` (checagem de permissão no client); exporta Excel.
- `/dashboard/perfil`: dados do usuário atual, badges de permissões, stats mock, dialog de edição.

### Integração com API
- Cliente `api` usa proxy `/api/backend`; inclui header `Authorization: Bearer <token>` se existir.
- Em erro 401, limpa token e redireciona para `/login`.

### Dependências e Stack
- Next.js 15, React 19, TypeScript, Tailwind v4, shadcn/Radix UI, TanStack Table, Recharts, DnD Kit, react-hook-form, zod, XLSX, sonner, tabler/lucide icons.

---

## Observações e Recomendações
- Restringir CORS em produção e definir `SECRET_KEY` seguro.
- Revisar rota `GET /api/v1/users/unidade/{unidade}` (retorno `None` hoje).
- Garantir roles mais rígidas no backend (algumas rotas de usuário não exigem auth além das marcadas).
- Proxy atual usa IP fixo `192.168.0.32`; parametrizar via env para ambientes diferentes.

