# Novos Endpoints da API - Backend

## Visão Geral

Foram implementados os endpoints para atender aos módulos do frontend:
- **Insurers** (Operadoras de Saúde)
- **Inventory Items** (Itens de Estoque)
- **Providers** (Prestadores de Serviços)
- **Reports** (Relatórios)

## Arquitetura Implementada

Seguindo os princípios de Clean Architecture e SOLID:

### Camada de Domínio
- **Entidades**: Insurer, InventoryItem, Provider, Report
- **Value Objects**: InsurerAddress, ProviderAddress, etc.
- **Repositories (Interfaces)**: Contratos para cada entidade

### Camada de Infraestrutura
- **Models SQLAlchemy**: Mapeamento ORM para PostgreSQL
- **Repositories Concretos**: Implementação com SQLAlchemy

### Camada de Aplicação
- **Use Cases**: Lógica de negócio isolada
  - Create, List, Update para cada módulo

### Camada de Apresentação
- **Routes Flask**: Endpoints REST API

## Endpoints Disponíveis

### Insurers (Operadoras de Saúde)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/insurers` | Listar operadoras (com filtros) |
| GET | `/api/v1/insurers/<id>` | Obter operadora por ID |
| POST | `/api/v1/insurers` | Criar nova operadora |
| PUT | `/api/v1/insurers/<id>` | Atualizar operadora |
| DELETE | `/api/v1/insurers/<id>` | Deletar operadora |

**Filtros disponíveis (GET list)**:
- `search`: Busca por nome, CNPJ
- `type`: Tipo de operadora (MEDICINA_GRUPO, COOPERATIVA, etc.)
- `status`: Status (ACTIVE, INACTIVE, SUSPENDED)
- `hasActivePlans`: Booleano
- `page`: Número da página
- `pageSize`: Tamanho da página

**Exemplo de criação**:
```json
POST /api/v1/insurers
{
  "name": "Sul América Seguros",
  "tradeName": "Sul América",
  "cnpj": "12.345.678/0001-90",
  "registrationNumber": "123456",
  "type": "MEDICINA_GRUPO",
  "phone": "(11) 3000-0000",
  "email": "contato@sulamerica.com.br",
  "website": "https://www.sulamerica.com.br",
  "address": {
    "street": "Av. Paulista",
    "number": "1000",
    "complement": "10º andar",
    "neighborhood": "Bela Vista",
    "city": "São Paulo",
    "state": "SP",
    "zipCode": "01310-100"
  }
}
```

### Inventory Items (Itens de Estoque)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/inventory-items` | Listar itens (com filtros) |
| GET | `/api/v1/inventory-items/<id>` | Obter item por ID |
| GET | `/api/v1/inventory-items/low-stock` | Itens com estoque baixo |

**Filtros disponíveis**:
- `search`: Busca por nome, código
- `category`: Categoria (MEDICATION, EQUIPMENT, SUPPLIES, CONSUMABLES)
- `status`: Status (AVAILABLE, LOW_STOCK, OUT_OF_STOCK, EXPIRED)
- `page`, `pageSize`: Paginação

### Providers (Prestadores de Serviços)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/providers` | Listar prestadores |
| GET | `/api/v1/providers/<id>` | Obter prestador por ID |

**Filtros disponíveis**:
- `search`: Busca por nome
- `page`, `pageSize`: Paginação

### Reports (Relatórios)

Utiliza o endpoint já existente em `/api/v1/reports`

## Migrações do Banco de Dados

Uma migration Alembic foi criada para adicionar as novas tabelas:

```bash
# Aplicar migration
alembic upgrade head

# Reverter migration
alembic downgrade -1
```

**Tabelas criadas**:
- `insurers`: Operadoras de saúde
- `inventory_items`: Itens de estoque
- `stock_movements`: Movimentações de estoque
- `providers`: Prestadores de serviços
- `reports`: Relatórios gerados

## Estrutura de Arquivos

```
src/
├── domain/
│   ├── entities/
│   │   ├── insurer.py
│   │   ├── inventory_item.py
│   │   ├── provider.py
│   │   └── report.py
│   └── repositories/
│       ├── insurer_repository.py
│       ├── inventory_item_repository.py
│       ├── provider_repository.py
│       └── report_repository.py
├── infrastructure/
│   ├── database/
│   │   └── models/
│   │       ├── insurer_model.py
│   │       ├── inventory_item_model.py
│   │       ├── provider_model.py
│   │       └── report_model.py
│   └── repositories/
│       ├── sqlalchemy_insurer_repository.py
│       ├── sqlalchemy_inventory_item_repository.py
│       ├── sqlalchemy_provider_repository.py
│       └── sqlalchemy_report_repository.py
├── application/
│   └── use_cases/
│       ├── insurers/
│       ├── inventory/
│       ├── providers/
│       └── reports/
└── presentation/
    └── api/
        └── v1/
            └── routes/
                ├── insurer_routes.py
                ├── inventory_item_routes.py
                ├── provider_routes.py
                └── reports_routes.py
```

## Próximos Passos

1. **Completar Use Cases**: Implementar use cases completos para Inventory, Providers e Reports
2. **Adicionar Validações**: Implementar validações mais robustas nos DTOs
3. **Testes**: Criar testes unitários e de integração
4. **Autenticação**: Adicionar middleware de autenticação nas rotas
5. **Documentação**: Gerar documentação Swagger/OpenAPI
6. **Melhorias**:
   - Implementar filtros JSON avançados (accepted_insurers, specialties)
   - Adicionar paginação cursor-based
   - Implementar cache com Redis
   - Adicionar rate limiting

## Como Usar

1. **Iniciar o backend**:
```bash
cd cuidar-plus-backend
python src/main.py
```

2. **Aplicar migrations**:
```bash
alembic upgrade head
```

3. **Testar endpoints**:
```bash
# Listar operadoras
curl http://localhost:5000/api/v1/insurers

# Listar itens de estoque
curl http://localhost:5000/api/v1/inventory-items

# Listar prestadores
curl http://localhost:5000/api/v1/providers
```

## Padrões Utilizados

- **Clean Architecture**: Separação clara de responsabilidades
- **SOLID**: Princípios aplicados em todas as camadas
- **Repository Pattern**: Abstração do acesso a dados
- **Use Case Pattern**: Lógica de negócio encapsulada
- **DTO Pattern**: Transferência de dados entre camadas
- **Dependency Injection**: Inversão de controle

## Notas Técnicas

- Todas as rotas assíncronas usam `async/await`
- Validações básicas implementadas nas entidades
- JSON usado para campos complexos (endereços, planos, etc.)
- Índices criados em campos de busca frequente
- Timestamps automáticos em todas as tabelas
