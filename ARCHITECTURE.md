# Arquitetura - Cuidar Plus Backend

## 📐 Visão Geral - Clean Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│  (Routes, Controllers, Middlewares, Schemas)                │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  Auth    │  │  Users   │  │ Patients │                 │
│  │  Routes  │  │  Routes  │  │  Routes  │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
└───────────────────┬──────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│         (Use Cases, DTOs, Business Logic)                   │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │  CreateUser    │  │ Authenticate   │  │ CreatePatient│ │
│  │  UseCase       │  │ UserUseCase    │  │  UseCase     │ │
│  └────────────────┘  └────────────────┘  └──────────────┘ │
└───────────────────┬──────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                            │
│    (Entities, Value Objects, Domain Services)               │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   User   │  │ Patient  │  │Medication│  │Appointment│ │
│  │  Entity  │  │  Entity  │  │  Entity  │  │  Entity   │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  Email   │  │   CPF    │  │  Phone   │                 │
│  │ValueObject│  │ValueObject│  │ValueObject│                │
│  └──────────┘  └──────────┘  └──────────┘                 │
│                                                              │
│  ┌────────────────────────────────────────────────┐        │
│  │         Repository Interfaces (Ports)          │        │
│  │  UserRepository, PatientRepository, etc.       │        │
│  └────────────────────────────────────────────────┘        │
└───────────────────┬──────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                        │
│  (Database, External Services, Implementations)             │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │  SQLAlchemy    │  │  Password      │  │  JWT         │ │
│  │  Repositories  │  │  Hasher        │  │  Handler     │ │
│  └────────────────┘  └────────────────┘  └──────────────┘ │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │  PostgreSQL    │  │    Redis       │  │  External    │ │
│  │   Database     │  │    Cache       │  │   APIs       │ │
│  └────────────────┘  └────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de uma Requisição

### Exemplo: Login de Usuário

```
1. CLIENT
   │
   │ POST /api/v1/auth/login
   │ { "email": "user@example.com", "password": "senha123" }
   │
   ▼
2. PRESENTATION LAYER
   │
   ├─▶ auth_routes.py (Route Handler)
   │   - Valida request
   │   - Cria AuthenticateUserInput DTO
   │
   ▼
3. APPLICATION LAYER
   │
   ├─▶ AuthenticateUserUseCase
   │   - Busca user no repository
   │   - Verifica senha (PasswordHasher)
   │   - Valida regras de negócio
   │   - Gera JWT tokens (JWTHandler)
   │   - Atualiza last_login
   │
   ▼
4. DOMAIN LAYER
   │
   ├─▶ User Entity
   │   - update_last_login() (business rule)
   │
   ├─▶ Email Value Object
   │   - Validação de email
   │
   ├─▶ UserRepository Interface
       - find_by_email(email)
       - save(user)
   │
   ▼
5. INFRASTRUCTURE LAYER
   │
   ├─▶ SQLAlchemyUserRepository
   │   - Implementa UserRepository
   │   - Converte Entity ↔ Model
   │
   ├─▶ UserModel (SQLAlchemy)
   │   - Mapeamento para tabela users
   │
   ├─▶ PostgreSQL Database
   │   - SELECT * FROM users WHERE email = ?
   │   - UPDATE users SET last_login = ?
   │
   ▼
6. RESPONSE
   │
   └─▶ CLIENT
       {
         "access_token": "eyJ0eXAi...",
         "refresh_token": "eyJ0eXAi...",
         "token_type": "Bearer",
         "expires_in": 3600
       }
```

---

## 🎯 Responsabilidades de Cada Camada

### Domain Layer (Núcleo)
**O QUE FAZ:**
- Define entidades de negócio (User, Patient, etc.)
- Contém regras de negócio (invariants)
- Value Objects para conceitos imutáveis
- Interfaces de repositório (contratos)

**NÃO SABE:**
- Como dados são persistidos
- Frameworks externos
- HTTP, JSON, etc.

**EXEMPLO:**
```python
class User:
    def deactivate(self):
        if not self.is_active:
            raise ValueError("User is already inactive")
        self.is_active = False
```

---

### Application Layer (Casos de Uso)
**O QUE FAZ:**
- Orquestra fluxo de use cases
- Coordena entre domain e infrastructure
- DTOs para input/output
- Lógica de aplicação (não de negócio)

**NÃO SABE:**
- Detalhes de HTTP
- Como UI funciona
- Implementações específicas de DB

**EXEMPLO:**
```python
class CreateUserUseCase:
    def execute(self, input_dto):
        # 1. Validar email único
        # 2. Hash password
        # 3. Criar entity
        # 4. Persistir
        # 5. Retornar output DTO
```

---

### Infrastructure Layer (Implementações)
**O QUE FAZ:**
- Implementa interfaces do domain
- Acessa banco de dados (SQLAlchemy)
- Integra com APIs externas
- Security (JWT, bcrypt)

**DEPENDE DE:**
- Domain layer (interfaces)
- Application layer (use cases)

**EXEMPLO:**
```python
class SQLAlchemyUserRepository(UserRepository):
    def find_by_email(self, email):
        model = self._session.query(UserModel)
                    .filter(UserModel.email == str(email))
                    .first()
        return self._to_entity(model)
```

---

### Presentation Layer (API)
**O QUE FAZ:**
- Recebe requests HTTP
- Valida input (schemas)
- Chama use cases
- Formata responses
- Middlewares (auth, errors)

**DEPENDE DE:**
- Application layer (use cases)

**EXEMPLO:**
```python
@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    input_dto = CreateUserInput(**data)
    output = use_case.execute(input_dto)
    return jsonify(output), 201
```

---

## 🔗 Dependency Flow (Inversão de Dependência)

```
PRESENTATION
    │
    ▼ depends on
APPLICATION
    │
    ▼ depends on (interfaces)
DOMAIN (núcleo - não depende de nada)
    ▲
    │ implements interfaces
INFRASTRUCTURE
```

**Regra de Ouro:**
- Dependências sempre apontam para dentro (domain)
- Domain não conhece camadas externas
- Infrastructure implementa interfaces do domain

---

## 📦 Entidades Principais

### User (Usuário)
```
User
├─ id: UUID
├─ email: Email (Value Object)
├─ password_hash: string
├─ full_name: string
├─ role: string (caregiver, family, admin)
├─ is_active: boolean
└─ Methods:
   ├─ create()
   ├─ deactivate()
   └─ update_last_login()
```

### Patient (Paciente)
```
Patient
├─ id: UUID
├─ caregiver_id: UUID
├─ full_name: string
├─ cpf: CPF (Value Object)
├─ date_of_birth: date
├─ gender: string
├─ medical_conditions: string
└─ Methods:
   ├─ create()
   ├─ get_age()
   └─ update_medical_info()
```

### Medication (Medicamento)
```
Medication
├─ id: UUID
├─ patient_id: UUID
├─ name: string
├─ dosage: string
├─ frequency: string
├─ schedule_times: list[time]
└─ Methods:
   ├─ create()
   ├─ deactivate()
   └─ update_schedule()
```

### Appointment (Consulta)
```
Appointment
├─ id: UUID
├─ patient_id: UUID
├─ title: string
├─ appointment_date: datetime
├─ status: string
└─ Methods:
   ├─ create()
   ├─ complete()
   ├─ cancel()
   └─ reschedule()
```

---

## 🗃️ Banco de Dados

### Tabelas Criadas:

```sql
users
├─ id (UUID, PK)
├─ email (VARCHAR, UNIQUE)
├─ password_hash (VARCHAR)
├─ full_name (VARCHAR)
├─ role (VARCHAR)
├─ is_active (BOOLEAN)
├─ created_at (TIMESTAMP)
├─ updated_at (TIMESTAMP)
└─ last_login (TIMESTAMP)

patients
├─ id (UUID, PK)
├─ caregiver_id (UUID, FK → users.id)
├─ full_name (VARCHAR)
├─ cpf (VARCHAR, UNIQUE)
├─ date_of_birth (DATE)
├─ gender (VARCHAR)
├─ address (TEXT)
├─ phone (VARCHAR)
├─ emergency_contact (VARCHAR)
├─ emergency_phone (VARCHAR)
├─ medical_conditions (TEXT)
├─ allergies (TEXT)
├─ observations (TEXT)
├─ is_active (BOOLEAN)
├─ created_at (TIMESTAMP)
└─ updated_at (TIMESTAMP)

medications
├─ id (UUID, PK)
├─ patient_id (UUID, FK → patients.id)
├─ name (VARCHAR)
├─ dosage (VARCHAR)
├─ frequency (VARCHAR)
├─ schedule_times (TIME[])
├─ start_date (TIMESTAMP)
├─ end_date (TIMESTAMP)
├─ instructions (TEXT)
├─ is_active (BOOLEAN)
├─ created_at (TIMESTAMP)
└─ updated_at (TIMESTAMP)

appointments
├─ id (UUID, PK)
├─ patient_id (UUID, FK → patients.id)
├─ title (VARCHAR)
├─ description (TEXT)
├─ appointment_date (TIMESTAMP)
├─ duration_minutes (INTEGER)
├─ location (VARCHAR)
├─ doctor_name (VARCHAR)
├─ specialty (VARCHAR)
├─ status (VARCHAR)
├─ reminder_sent (BOOLEAN)
├─ created_at (TIMESTAMP)
└─ updated_at (TIMESTAMP)
```

---

## 🔐 Autenticação JWT

### Fluxo de Autenticação:

```
1. Login
   POST /api/v1/auth/login
   { email, password }
   │
   ▼
   Retorna: { access_token, refresh_token }

2. Request Protegida
   GET /api/v1/users/{id}
   Header: Authorization: Bearer {access_token}
   │
   ▼
   Middleware valida token
   │
   ▼
   Request procede com user_id no contexto

3. Refresh Token
   POST /api/v1/auth/refresh
   { refresh_token }
   │
   ▼
   Retorna: { access_token }
```

### Token Structure:
```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "role": "caregiver",
  "exp": 1234567890,
  "iat": 1234564290,
  "type": "access"
}
```

---

## 📝 Padrões e Convenções

### Naming Conventions:
- **Entities**: PascalCase (User, Patient)
- **Value Objects**: PascalCase (Email, CPF)
- **Use Cases**: PascalCase com sufixo UseCase (CreateUserUseCase)
- **Repositories**: PascalCase com sufixo Repository (UserRepository)
- **Routes**: snake_case para funções (create_user, get_patient)
- **DTOs**: PascalCase com sufixo Input/Output (CreateUserInput)

### File Organization:
- Um arquivo por classe/entidade
- __init__.py em cada package
- Tests espelham estrutura de src/

### Error Handling:
- **DomainException**: Erros de regra de negócio
- **ApplicationException**: Erros de use case
- **ValueError**: Erros de validação
- **HTTPException**: Erros HTTP (404, 401, etc.)

---

**Autor**: GitHub Copilot  
**Versão**: 1.0  
**Data**: Janeiro 2026
