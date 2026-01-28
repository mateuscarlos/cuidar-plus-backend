# Guia de Início Rápido - Cuidar Plus Backend

## 🚀 Setup Inicial

### 1. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
# Mínimo necessário para rodar localmente:
# - SECRET_KEY
# - JWT_SECRET_KEY
# - DATABASE_URL
```

### 4. Inicializar Banco de Dados

```bash
# Opção 1: Usar script Python
python scripts/init_db.py

# Opção 2: Usar Alembic (recomendado para produção)
alembic upgrade head
```

### 5. Iniciar o Servidor

```bash
# Modo desenvolvimento
flask run

# Ou usar o script Python diretamente
python src/main.py
```

O servidor estará rodando em: **http://localhost:5000**

---

## 🐳 Docker Setup (Recomendado)

### Iniciar com Docker Compose

```bash
# Iniciar todos os serviços (backend, postgres, redis)
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Parar serviços
docker-compose down
```

**Serviços disponíveis:**
- Backend: http://localhost:5000
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- pgAdmin: http://localhost:5050 (admin@cuidarplus.com / admin)

---

## 📡 Endpoints Principais

### Health Check
```bash
GET http://localhost:5000/health
```

### Autenticação

**Login (obter token JWT):**
```bash
POST http://localhost:5000/api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@cuidarplus.com",
  "password": "admin123"
}
```

**Refresh Token:**
```bash
POST http://localhost:5000/api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "seu_refresh_token"
}
```

### Usuários

**Criar usuário:**
```bash
POST http://localhost:5000/api/v1/users/
Content-Type: application/json

{
  "email": "caregiver@example.com",
  "password": "senha123",
  "full_name": "João Silva",
  "role": "caregiver"
}
```

**Buscar usuário:**
```bash
GET http://localhost:5000/api/v1/users/{user_id}
Authorization: Bearer {access_token}
```

### Pacientes

**Criar paciente:**
```bash
POST http://localhost:5000/api/v1/patients/
Content-Type: application/json
Authorization: Bearer {access_token}

{
  "caregiver_id": "uuid-do-cuidador",
  "full_name": "Maria Silva",
  "cpf": "111.444.777-35",
  "date_of_birth": "1950-05-15",
  "gender": "F",
  "address": "Rua Example, 123",
  "phone": "(11) 98765-4321",
  "emergency_contact": "João Silva",
  "emergency_phone": "(11) 91234-5678",
  "medical_conditions": "Hipertensão, Diabetes",
  "allergies": "Penicilina"
}
```

**Listar pacientes do cuidador:**
```bash
GET http://localhost:5000/api/v1/patients/caregiver/{caregiver_id}
Authorization: Bearer {access_token}
```

---

## 🧪 Testes

### Executar todos os testes
```bash
pytest
```

### Executar com cobertura
```bash
pytest --cov=src --cov-report=html
```

### Executar apenas testes unitários
```bash
pytest tests/unit/ -v
```

### Executar apenas testes de integração
```bash
pytest tests/integration/ -v
```

---

## 📊 Banco de Dados

### Criar nova migration
```bash
alembic revision --autogenerate -m "Descrição da mudança"
```

### Aplicar migrations
```bash
alembic upgrade head
```

### Reverter última migration
```bash
alembic downgrade -1
```

### Ver histórico de migrations
```bash
alembic history
```

---

## 🔧 Comandos Úteis

### Formatar código
```bash
ruff format .
```

### Verificar linting
```bash
ruff check .
```

### Type checking
```bash
mypy src/
```

### Instalar pre-commit hooks
```bash
pre-commit install
```

---

## 📝 Estrutura de Autenticação

1. **Login** → Obter `access_token` e `refresh_token`
2. **Requisições protegidas** → Incluir header:
   ```
   Authorization: Bearer {access_token}
   ```
3. **Token expirado** → Usar `refresh_token` para obter novo `access_token`

---

## 🔒 Usuário Padrão

Após inicializar o banco, existe um usuário admin:

- **Email:** admin@cuidarplus.com
- **Senha:** admin123

⚠️ **IMPORTANTE:** Mude a senha em produção!

---

## 📚 Documentação Adicional

- [Arquitetura Clean Architecture](docs/architecture.md)
- [Guia de Contribuição](docs/contributing.md)
- [API Reference](http://localhost:5000/api/docs)

---

## ❓ Troubleshooting

### Erro de conexão com banco de dados
```bash
# Verificar se PostgreSQL está rodando
docker-compose ps

# Reiniciar serviços
docker-compose restart db
```

### Erro de migrations
```bash
# Resetar banco (CUIDADO: apaga todos os dados!)
python scripts/init_db.py --drop
alembic upgrade head
```

### Problemas com dependências
```bash
# Reinstalar dependências
pip install --upgrade --force-reinstall -r requirements.txt
```

---

**Suporte:** team@cuidarplus.com
