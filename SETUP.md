# Setup Instructions - Cuidar Plus Backend

## ✅ O que foi criado

Backend completo da aplicação **Cuidar Plus** seguindo **Clean Architecture** com:

### 📂 Estrutura de Diretórios

```
backend/
├── src/
│   ├── domain/              ✅ Entities, Value Objects, Repository Interfaces
│   ├── application/         ✅ Use Cases, DTOs, Application Services
│   ├── infrastructure/      ✅ Database, Repositories, Security, External Services
│   ├── presentation/        ✅ API Routes, Middlewares, Schemas
│   ├── shared/             ✅ Exceptions, Utils, Decorators
│   ├── config.py           ✅ Configurações centralizadas
│   └── main.py             ✅ Entry point da aplicação
├── tests/                   ✅ Testes unitários, integração e E2E
├── scripts/                 ✅ Scripts de inicialização
├── requirements.txt         ✅ Dependências Python
├── docker-compose.yml       ✅ Setup Docker
├── Dockerfile              ✅ Container da aplicação
└── README.md               ✅ Documentação

```

### 🎯 Funcionalidades Implementadas

#### Domain Layer (Domínio)
- ✅ **Entities**: User, Patient, Medication, Appointment
- ✅ **Value Objects**: Email, CPF, Phone (com validações)
- ✅ **Repository Interfaces**: Contratos para persistência
- ✅ **Domain Services**: MedicationScheduler

#### Application Layer (Aplicação)
- ✅ **Use Cases**:
  - CreateUser, AuthenticateUser, GetUserById
  - CreatePatient, ListPatients
  - CreateMedication
- ✅ **DTOs**: Input/Output para cada use case
- ✅ **Interfaces**: Email, SMS, Storage services

#### Infrastructure Layer (Infraestrutura)
- ✅ **Database**: SQLAlchemy + PostgreSQL
- ✅ **Models**: UserModel, PatientModel, MedicationModel, AppointmentModel
- ✅ **Repositories**: Implementações concretas dos repositórios
- ✅ **Security**: PasswordHasher (bcrypt), JWTHandler
- ✅ **Migrations**: Alembic configurado

#### Presentation Layer (Apresentação)
- ✅ **Routes**:
  - `/api/v1/auth/*` - Autenticação (login, refresh)
  - `/api/v1/users/*` - Gerenciamento de usuários
  - `/api/v1/patients/*` - Gerenciamento de pacientes
- ✅ **Middlewares**: Autenticação JWT, Error Handler
- ✅ **CORS**: Configurado para frontend

#### Shared Layer (Compartilhado)
- ✅ **Exceptions**: DomainException, ApplicationException
- ✅ **Utils**: Logger estruturado
- ✅ **Decorators**: Transactional

---

## 🚀 Como Executar

### Opção 1: Docker (Recomendado)

```bash
# 1. Copiar variáveis de ambiente
cp .env.example .env

# 2. Iniciar todos os serviços
docker-compose up -d

# 3. Verificar se está rodando
curl http://localhost:5000/health
```

### Opção 2: Local

```bash
# 1. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar .env
cp .env.example .env
# Editar .env com DATABASE_URL, JWT_SECRET_KEY, etc.

# 4. Inicializar banco
python scripts/init_db.py

# 5. Executar aplicação
flask run
# ou
python src/main.py
```

---

## 🧪 Testar a API

### 1. Health Check
```bash
curl http://localhost:5000/health
```

### 2. Criar usuário
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@example.com",
    "password": "senha123",
    "full_name": "Teste User",
    "role": "caregiver"
  }'
```

### 3. Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@cuidarplus.com",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAi...",
  "refresh_token": "eyJ0eXAi...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### 4. Buscar usuário (com autenticação)
```bash
curl http://localhost:5000/api/v1/users/{user_id} \
  -H "Authorization: Bearer {access_token}"
```

---

## 📝 Próximos Passos

### Para Produção:
1. ⚠️ **Mudar senhas padrão** (.env)
2. ⚠️ **Configurar SECRET_KEY e JWT_SECRET_KEY** seguros
3. ✅ Configurar serviços externos (Email, SMS, S3)
4. ✅ Implementar rate limiting
5. ✅ Adicionar logging estruturado
6. ✅ Configurar CI/CD
7. ✅ Implementar testes E2E completos
8. ✅ Documentar API com Swagger/OpenAPI

### Funcionalidades Adicionais:
- Endpoints de Medications completos
- Endpoints de Appointments
- Notificações por email/SMS
- Upload de arquivos (fotos, documentos)
- Dashboard de métricas
- Relatórios

---

## 📊 Banco de Dados

### Modelos Criados:
- ✅ `users` - Usuários do sistema
- ✅ `patients` - Pacientes/Idosos
- ✅ `medications` - Medicamentos
- ✅ `appointments` - Consultas médicas

### Migrations:
```bash
# Criar migration
alembic revision --autogenerate -m "Initial schema"

# Aplicar migrations
alembic upgrade head

# Reverter
alembic downgrade -1
```

---

## 🔐 Autenticação

Sistema usa **JWT (JSON Web Tokens)** com:
- **Access Token**: Expira em 1 hora
- **Refresh Token**: Expira em 30 dias

Rotas protegidas requerem header:
```
Authorization: Bearer {access_token}
```

---

## 🧪 Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Apenas unitários
pytest tests/unit/ -v

# Apenas integração
pytest tests/integration/ -v
```

### Testes Implementados:
- ✅ User Entity
- ✅ Email Value Object
- ✅ CPF Value Object
- 📝 Adicionar mais testes conforme necessário

---

## 📚 Arquitetura

### Princípios Aplicados:
- ✅ **Clean Architecture** - Separação de responsabilidades
- ✅ **SOLID** - Princípios de design OO
- ✅ **DDD** - Domain-Driven Design
- ✅ **Dependency Inversion** - Dependências apontam para abstrações

### Fluxo de Requisição:
```
Request → Route → Use Case → Repository → Database
                     ↓
                  Domain Entity (business rules)
```

---

## 🛠️ Tecnologias

- **Python 3.12+**
- **Flask 3.1+** - Web Framework
- **SQLAlchemy 2.0+** - ORM
- **PostgreSQL 16+** - Database
- **Redis 7+** - Cache
- **Pydantic 2.10+** - Validation
- **PyJWT** - Authentication
- **Alembic** - Migrations
- **pytest** - Testing
- **Docker** - Containerization

---

## ⚠️ Avisos Importantes

1. **Senha padrão do admin**: `admin123` - **MUDAR EM PRODUÇÃO!**
2. **SECRET_KEY**: Gerar uma chave segura para produção
3. **DATABASE_URL**: Configurar banco de produção
4. **CORS_ORIGINS**: Ajustar para domínio de produção
5. **Logs**: Configurar sistema de logs centralizado

---

## 📞 Suporte

- **Email**: team@cuidarplus.com
- **Documentação**: Veja README.md e QUICKSTART.md
- **Issues**: Abra uma issue no repositório

---

**Versão**: 1.0.0  
**Data**: Janeiro 2026  
**Status**: ✅ Pronto para desenvolvimento
