# Domain Services

## 📘 O Que São Domain Services?

Domain Services são classes que encapsulam **regras de negócio** que não pertencem naturalmente a uma única entidade. Eles complementam as entidades (Entities) quando a lógica de negócio:

- Envolve múltiplas entidades
- É complexa demais para ficar em uma entidade
- Não é responsabilidade de uma entidade específica
- Precisa ser reutilizada em vários Use Cases

## 🎯 Quando Usar Domain Services?

### ✅ USE Domain Services quando:

- **Validações complexas:** CPF, CNPJ, algoritmos matemáticos
- **Cálculos de negócio:** Idade, disponibilidade, níveis de risco
- **Regras multi-entidade:** Verificar se pode desativar baseado em relacionamentos
- **Lógica reutilizável:** Mesma regra usada em vários lugares
- **Operações sem estado:** Métodos estáticos que não alteram o estado

### ❌ NÃO USE Domain Services para:

- **Operações de CRUD simples:** Use Use Cases diretamente
- **Lógica de persistência:** Use Repositories
- **Transformação de dados:** Use DTOs ou Mappers
- **Lógica de apresentação:** Use Controllers
- **Orquestração:** Use Use Cases

## 📁 Estrutura de Arquivos

```
src/domain/services/
├── __init__.py                    # Exports
├── insurer_service.py            # Regras de Operadoras
├── inventory_service.py          # Regras de Estoque
├── provider_service.py           # Regras de Prestadores
├── report_service.py             # Regras de Relatórios
└── patient_service.py            # Regras de Pacientes
```

## 🏗️ Arquitetura

### Padrão Domain Service

```python
class XxxDomainService:
    """Domain Service for Xxx business rules."""
    
    @staticmethod
    def validate_for_creation(...) -> List[str]:
        """
        Validate data before creating entity.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Business validations
        if not name:
            errors.append("Nome obrigatório")
        
        return errors
    
    @staticmethod
    def can_perform_action(entity: Xxx) -> Tuple[bool, str]:
        """
        Check if action can be performed.
        
        Returns:
            (can_do, reason)
        """
        if entity.has_dependency():
            return False, "Não pode: tem dependências"
        
        return True, "Pode realizar ação"
    
    @staticmethod
    def calculate_business_value(entity: Xxx) -> float:
        """
        Calculate business metric.
        
        Returns:
            Calculated value
        """
        return entity.field1 * entity.field2
```

### Características

1. **Stateless (Sem Estado)**
   - Todos os métodos são `@staticmethod`
   - Não mantêm estado interno
   - Recebem dados via parâmetros

2. **Pure Functions (Funções Puras)**
   - Mesma entrada → mesma saída
   - Sem efeitos colaterais
   - Fácil de testar

3. **Self-Contained (Auto-contido)**
   - Não dependem de infraestrutura
   - Não dependem de frameworks
   - Apenas lógica de negócio pura

## 📚 Services Implementados

### 1. InsurerDomainService

**Responsabilidade:** Regras de negócio para Operadoras de Saúde

**Principais Métodos:**
- `validate_cnpj(cnpj: str) -> bool`: Valida CNPJ com dígitos verificadores
- `validate_for_creation(...)`: Valida dados antes de criar operadora
- `can_be_deactivated(insurer)`: Verifica se pode desativar
- `can_add_plans(insurer)`: Verifica se pode adicionar planos

**Regras Principais:**
- CNPJ deve ser válido (14 dígitos + check digits)
- Número ANS deve ter 6 dígitos
- Não pode desativar se tiver planos ativos

---

### 2. InventoryDomainService

**Responsabilidade:** Regras de gestão de estoque

**Principais Métodos:**
- `calculate_status(item)`: Calcula status automaticamente
- `is_low_stock(item)`: Verifica se estoque está baixo
- `is_expired(item)`: Verifica se item está vencido
- `is_near_expiration(item, days)`: Verifica vencimento próximo
- `can_perform_output(item, quantity)`: Valida saída de estoque
- `calculate_reorder_quantity(item)`: Calcula quanto repor

**Regras Principais:**
- Status: OUT_OF_STOCK (0), LOW_STOCK (≤mín), IN_STOCK (>mín)
- Não pode dar saída de item vencido
- Alerta de vencimento próximo: 30 dias

---

### 3. ProviderDomainService

**Responsabilidade:** Regras para Prestadores de Serviços

**Principais Métodos:**
- `validate_cpf(cpf)`: Valida CPF com dígitos verificadores
- `validate_cnpj(cnpj)`: Valida CNPJ com dígitos verificadores
- `validate_document(doc)`: Detecta e valida CPF ou CNPJ
- `has_valid_credentials(provider)`: Verifica credenciais válidas
- `calculate_availability(provider)`: Calcula disponibilidade (0-100%)
- `can_be_deactivated(provider)`: Verifica se pode desativar

**Regras Principais:**
- CPF: 11 dígitos + validação mod 11
- CNPJ: 14 dígitos + validação mod 11
- Disponibilidade baseada em: horários, credenciais, especialidades, operadoras

---

### 4. ReportDomainService

**Responsabilidade:** Regras para geração de relatórios

**Principais Métodos:**
- `validate_for_creation(type, start, end)`: Valida antes de criar
- `get_default_date_range(period)`: Retorna intervalo padrão
- `estimate_generation_time(type, start, end)`: Estima tempo
- `can_regenerate(report)`: Verifica se pode regenerar

**Regras Principais:**
- Intervalo máximo: 5 anos
- Data fim ≥ data início
- Períodos padrão: DAILY, WEEKLY, MONTHLY, QUARTERLY, YEARLY

---

### 5. PatientDomainService

**Responsabilidade:** Regras para gestão de pacientes

**Principais Métodos:**
- `validate_cpf(cpf)`: Valida CPF do paciente
- `calculate_age(birth_date)`: Calcula idade precisa
- `is_pediatric(patient)`: Verifica se é pediátrico (<18)
- `is_elderly(patient)`: Verifica se é idoso (≥65)
- `get_risk_level(patient)`: Retorna HIGH/MEDIUM/LOW
- `requires_companion(patient)`: Verifica necessidade de acompanhante

**Regras Principais:**
- Pediátrico: <18 anos (requer acompanhante)
- Idoso: ≥65 anos (requer acompanhante)
- Risco: HIGH (≥65 ou doenças crônicas), MEDIUM (45-64), LOW (<45)

## 🔄 Fluxo de Uso

```
┌─────────────────┐
│   Controller    │  1. Recebe request
│   (API Route)   │
└────────┬────────┘
         │
         │ 2. Chama Use Case
         ▼
┌─────────────────┐
│    Use Case     │  3. Orquestra operação
└────────┬────────┘
         │
         │ 4. Valida com Domain Service
         ▼
┌─────────────────┐
│ Domain Service  │  5. Aplica regras de negócio
│   (Stateless)   │     Retorna erros ou OK
└────────┬────────┘
         │
         │ 6. Se OK, continua
         ▼
┌─────────────────┐
│     Entity      │  7. Cria/atualiza entidade
└────────┬────────┘
         │
         │ 8. Persiste
         ▼
┌─────────────────┐
│   Repository    │  9. Salva no banco
└─────────────────┘
```

### Exemplo Completo

```python
# 1. Controller/Route
@app.post('/insurers')
async def create_insurer(data: dict):
    use_case = CreateInsurerUseCase(repository)
    result = await use_case.execute(data)
    return result

# 2. Use Case
class CreateInsurerUseCase:
    async def execute(self, input_dto):
        # 3. Valida com Domain Service
        errors = InsurerDomainService.validate_for_creation(
            name=input_dto.name,
            cnpj=input_dto.cnpj,
            ...
        )
        if errors:
            raise ValidationException(errors)
        
        # 4. Valida CNPJ
        if not InsurerDomainService.validate_cnpj(input_dto.cnpj):
            raise ValidationException("CNPJ inválido")
        
        # 5. Verifica duplicatas (Repository)
        existing = await self._repository.get_by_cnpj(input_dto.cnpj)
        if existing:
            raise DuplicateException("CNPJ já existe")
        
        # 6. Cria Entity
        insurer = Insurer.create(...)
        
        # 7. Persiste
        return await self._repository.create(insurer)
```

## ✅ Boas Práticas

### 1. Nomenclatura

```python
# ✅ BOM: Verbo que descreve ação
InsurerDomainService.validate_cnpj(cnpj)
InsurerDomainService.can_be_deactivated(insurer)
InventoryDomainService.calculate_status(item)

# ❌ RUIM: Nome genérico
InsurerDomainService.check(insurer)
InsurerDomainService.process(data)
```

### 2. Retorno de Erros

```python
# ✅ BOM: Lista de erros para validações
def validate_for_creation(...) -> List[str]:
    errors = []
    if not name:
        errors.append("Nome obrigatório")
    return errors  # [] se válido

# ✅ BOM: Tupla (bool, str) para verificações
def can_be_deactivated(entity) -> Tuple[bool, str]:
    if entity.has_plans:
        return False, "Não pode: tem planos ativos"
    return True, "Pode desativar"

# ❌ RUIM: Exceções em Domain Service
def validate(...):
    if not valid:
        raise Exception()  # Não!
```

### 3. Documentação

```python
# ✅ BOM: Documentação clara
def calculate_age(birth_date: date) -> int:
    """
    Calculate age in years.
    
    Args:
        birth_date: Date of birth
        
    Returns:
        Age in complete years
        
    Example:
        >>> calculate_age(date(2000, 1, 1))
        24
    """
```

### 4. Testes

```python
# ✅ BOM: Testes isolados
def test_validate_cnpj_valid():
    # Arrange
    cnpj = "11222333000181"
    
    # Act
    is_valid = InsurerDomainService.validate_cnpj(cnpj)
    
    # Assert
    assert is_valid

def test_can_be_deactivated_with_active_plans():
    # Arrange
    insurer = Insurer(...)
    insurer.add_plan(...)
    
    # Act
    can_deactivate, reason = InsurerDomainService.can_be_deactivated(insurer)
    
    # Assert
    assert not can_deactivate
    assert "planos ativos" in reason.lower()
```

## 🚫 Anti-Padrões

### 1. Domain Service com Estado

```python
# ❌ RUIM: Mantém estado
class BadDomainService:
    def __init__(self):
        self.cache = {}  # Estado!
    
    def validate(self, data):
        self.cache[data.id] = data  # Efeito colateral!

# ✅ BOM: Stateless
class GoodDomainService:
    @staticmethod
    def validate(data):
        # Apenas validação pura
        return data.is_valid()
```

### 2. Dependências de Infraestrutura

```python
# ❌ RUIM: Depende de banco/framework
class BadDomainService:
    def __init__(self, db):
        self.db = db
    
    def validate(self, data):
        existing = self.db.query(...)  # Não!

# ✅ BOM: Sem dependências
class GoodDomainService:
    @staticmethod
    def validate(data):
        # Apenas lógica pura
        return len(data) > 0
```

### 3. Lógica de Orquestração

```python
# ❌ RUIM: Orquestra múltiplas operações
class BadDomainService:
    @staticmethod
    def create_with_plans(data):
        insurer = Insurer.create(...)
        for plan in data.plans:
            insurer.add_plan(plan)
        # Salva, envia email, etc...  # Não!

# ✅ BOM: Apenas validação/cálculo
class GoodDomainService:
    @staticmethod
    def validate_for_creation(data):
        # Apenas valida
        return [] if data.is_valid else ["Erro"]
```

## 📖 Referências

- **Clean Architecture** (Robert C. Martin)
  - Domain Services na camada de domínio
  - Independente de frameworks e infraestrutura

- **Domain-Driven Design** (Eric Evans)
  - Domain Services para lógica que não pertence a entidades
  - Mantém o domínio focado

- **SOLID Principles**
  - **Single Responsibility:** Cada service tem uma responsabilidade
  - **Open/Closed:** Extensível via novos services
  - **Dependency Inversion:** Não depende de implementações

## 🎓 Quando Criar um Novo Domain Service?

### Checklist:

1. ✅ A lógica envolve regras de negócio complexas?
2. ✅ A lógica não pertence a uma única entidade?
3. ✅ A lógica será reutilizada em múltiplos Use Cases?
4. ✅ A lógica pode ser testada isoladamente?
5. ✅ A lógica não precisa acessar banco de dados?

Se responder **SIM** para 3+ perguntas → **Crie um Domain Service**

### Template:

```python
"""XxxDomainService - Business Rules for Xxx."""
from typing import List, Tuple


class XxxDomainService:
    """
    Domain Service for Xxx business rules.
    
    Encapsulates business logic that doesn't belong to a single entity.
    """
    
    @staticmethod
    def validate_for_creation(...) -> List[str]:
        """
        Validate data before creating Xxx.
        
        Args:
            ...: Description
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Add validations
        if not field:
            errors.append("Field is required")
        
        return errors
    
    @staticmethod
    def can_perform_action(entity: Xxx) -> Tuple[bool, str]:
        """
        Check if action can be performed on Xxx.
        
        Args:
            entity: Xxx entity to check
            
        Returns:
            (can_perform, reason)
        """
        if entity.has_blocker():
            return False, "Cannot: has blocker"
        
        return True, "Action can be performed"
```

---

**Versão:** 1.0.0  
**Última Atualização:** Janeiro 2024  
**Autor:** Sistema Cuidar Plus
