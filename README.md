# Cuidar Plus - Backend

Backend para sistema de cuidado de idosos desenvolvido em Python/Flask seguindo Clean Architecture.

## 🏗️ Arquitetura

Este projeto segue os princípios de **Clean Architecture** e **SOLID**, com separação clara entre camadas:

- **Domain**: Entidades, Value Objects, Interfaces de Repositório
- **Application**: Use Cases, DTOs, Lógica de Aplicação
- **Infrastructure**: Implementações concretas (DB, APIs externas)
- **Presentation**: Controllers, Routes, Schemas de API

## 🚀 Stack Tecnológica

- **Python 3.12+**
- **Flask 3.1+** - Web Framework
- **SQLAlchemy 2.0+** - ORM
- **PostgreSQL 16+** - Banco de Dados
- **Redis 7+** - Cache
- **Pydantic 2.10+** - Validação
- **PyJWT** - Autenticação
- **pytest** - Testes

## 📦 Instalação

### Pré-requisitos

- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- Docker e Docker Compose (opcional)

### Setup Local

1. **Clone o repositório**

```bash
git clone https://github.com/your-org/cuidar-plus-backend.git
cd cuidar-plus-backend
```

2. **Crie um ambiente virtual**

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. **Execute as migrações do banco**

```bash
alembic upgrade head
```

6. **Inicie o servidor**

```bash
flask run
```

## 🐳 Docker

### Executar com Docker Compose

```bash
docker-compose up -d
```

Isso irá iniciar:
- Backend na porta 5000
- PostgreSQL na porta 5432
- Redis na porta 6379

## 🧪 Testes

### Executar todos os testes

```bash
pytest
```

### Executar testes com cobertura

```bash
pytest --cov=src --cov-report=html
```

### Executar apenas testes unitários

```bash
pytest -m unit
```

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:5000/api/docs
- **ReDoc**: http://localhost:5000/api/redoc

## 🗂️ Estrutura do Projeto

```
backend/
├── src/
│   ├── domain/              # Camada de Domínio
│   ├── application/         # Camada de Aplicação
│   ├── infrastructure/      # Camada de Infraestrutura
│   ├── presentation/        # Camada de Apresentação
│   ├── shared/              # Código Compartilhado
│   ├── main.py             # Entry Point
│   └── config.py           # Configurações
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## 🔒 Segurança

- Senhas hasheadas com bcrypt
- Autenticação via JWT
- CORS configurável
- Validação de dados com Pydantic

## 📝 Licença

Este projeto está sob a licença MIT.

## 👥 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📧 Contato

Cuidar Plus Team - team@cuidarplus.com
