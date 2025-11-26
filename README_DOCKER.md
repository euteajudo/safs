# Docker Setup para SAFS

Este documento explica como configurar o banco de dados PostgreSQL usando Docker para o projeto SAFS.

## 🐳 Configuração do Docker

### 1. Pré-requisitos
- Docker instalado
- Docker Compose instalado

### 2. Serviços Incluídos

#### PostgreSQL 16 Alpine
- **Imagem**: `postgres:16-alpine` (estável, leve e com LTS)
- **Porta**: 5432
- **Banco**: safs_db
- **Usuário**: safs_user
- **Senha**: safs_password

#### PgAdmin 4 (Interface Web)
- **Porta**: 8080
- **Email**: admin@safs.local
- **Senha**: admin123

### 3. Comandos para Executar

#### Iniciar os serviços
```bash
docker-compose up -d
```

#### Parar os serviços
```bash
docker-compose down
```

#### Ver logs
```bash
docker-compose logs -f postgres
docker-compose logs -f pgadmin
```

#### Reiniciar apenas o PostgreSQL
```bash
docker-compose restart postgres
```

### 4. Configuração da Aplicação

#### Backend (FastAPI)
1. Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```

2. A URL de conexão já está configurada:
```
DATABASE_URL=postgresql://safs_user:safs_password@localhost:5432/safs_db
```

#### Acessar PgAdmin
1. Abra: http://localhost:8080
2. Login: admin@safs.local
3. Senha: admin123
4. Adicione servidor:
   - Host: postgres (ou localhost se acessando externamente)
   - Port: 5432
   - Database: safs_db
   - Username: safs_user
   - Password: safs_password

### 5. Volumes e Persistência

Os dados são persistidos em volumes Docker:
- `postgres_data`: Dados do PostgreSQL
- `pgadmin_data`: Configurações do PgAdmin

### 6. Rede

Os serviços estão em uma rede interna `safs_network` para comunicação segura.

### 7. Health Check

O PostgreSQL possui health check configurado para garantir que está funcionando antes de outros serviços tentarem conectar.

### 8. Comandos Úteis

#### Conectar diretamente ao banco via psql
```bash
docker exec -it safs_postgres psql -U safs_user -d safs_db
```

#### Backup do banco
```bash
docker exec safs_postgres pg_dump -U safs_user safs_db > backup.sql
```

#### Restaurar backup
```bash
docker exec -i safs_postgres psql -U safs_user -d safs_db < backup.sql
```

### 9. Produção

Para produção, altere:
- Senhas mais seguras
- Remova o PgAdmin se não necessário
- Configure SSL/TLS
- Use secrets do Docker Swarm ou Kubernetes