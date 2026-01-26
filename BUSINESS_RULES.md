# Regras de Negócio - Backend

Este documento descreve todas as regras de negócio migradas do frontend para o backend, centralizadas nos Domain Services seguindo os princípios de Clean Architecture e DDD.

## 📋 Índice

1. [Operadoras (Insurers)](#operadoras-insurers)
2. [Estoque (Inventory)](#estoque-inventory)
3. [Prestadores (Providers)](#prestadores-providers)
4. [Relatórios (Reports)](#relatórios-reports)
5. [Pacientes (Patients)](#pacientes-patients)

---

## 🏥 Operadoras (Insurers)

**Arquivo:** `src/domain/services/insurer_service.py`

### Validações

#### 1. Validação de CNPJ
- **Regra:** CNPJ deve ter 14 dígitos numéricos
- **Validação:** Algoritmo completo de dígitos verificadores
- **Método:** `validate_cnpj(cnpj: str) -> bool`
- **Processo:**
  1. Remove caracteres não numéricos
  2. Verifica se tem exatamente 14 dígitos
  3. Rejeita CNPJs com todos os dígitos iguais
  4. Calcula e valida o primeiro dígito verificador
  5. Calcula e valida o segundo dígito verificador

**Exemplo:**
```python
# CNPJ válido: 11.222.333/0001-81
is_valid = InsurerDomainService.validate_cnpj("11.222.333/0001-81")
# Retorna: True (dígitos verificadores 81 estão corretos)
```

#### 2. Validação de Criação
- **Método:** `validate_for_creation(...) -> List[str]`
- **Regras:**
  - Nome obrigatório
  - CNPJ obrigatório e válido
  - Número ANS obrigatório e com 6 dígitos
  - Email obrigatório e com formato válido
  - Telefone obrigatório

**Exemplo:**
```python
errors = InsurerDomainService.validate_for_creation(
    name="Operadora Exemplo",
    cnpj="11222333000181",
    registration_number="12345",  # Erro: deve ter 6 dígitos
    email="invalido",  # Erro: formato inválido
    phone="",  # Erro: obrigatório
)
# Retorna: ["ANS deve ter 6 dígitos", "Email inválido", "Telefone obrigatório"]
```

### Operações

#### 3. Desativação
- **Regra:** Operadora só pode ser desativada se não tiver planos ativos
- **Método:** `can_be_deactivated(insurer: Insurer) -> Tuple[bool, str]`
- **Retorno:** `(pode_desativar, motivo)`

**Exemplo:**
```python
can_deactivate, reason = InsurerDomainService.can_be_deactivated(operadora)
if not can_deactivate:
    raise Exception(reason)  # "Não é possível desativar: possui X planos ativos"
```

#### 4. Adição de Planos
- **Regra:** Só pode adicionar planos se operadora estiver ativa
- **Método:** `can_add_plans(insurer: Insurer) -> Tuple[bool, str]`

---

## 📦 Estoque (Inventory)

**Arquivo:** `src/domain/services/inventory_service.py`

### Gestão de Estoque

#### 1. Status Automático
- **Método:** `calculate_status(item: InventoryItem) -> ItemStatus`
- **Regras:**
  - `OUT_OF_STOCK`: quantidade = 0
  - `LOW_STOCK`: quantidade ≤ estoque mínimo
  - `IN_STOCK`: quantidade > estoque mínimo
  - `RESERVED`: se houver quantidades reservadas

**Exemplo:**
```python
status = InventoryDomainService.calculate_status(item)
# Se item.quantity = 5 e item.minimum_quantity = 10
# Retorna: ItemStatus.LOW_STOCK
```

#### 2. Verificação de Estoque Baixo
- **Método:** `is_low_stock(item: InventoryItem) -> bool`
- **Regra:** Retorna `True` se quantidade ≤ estoque mínimo

#### 3. Cálculo de Reposição
- **Método:** `calculate_reorder_quantity(item: InventoryItem) -> float`
- **Regra:** Calcula quanto pedir para atingir o estoque ideal
- **Fórmula:** `max(0, ideal_quantity - current_quantity)`

**Exemplo:**
```python
# Item com quantidade=5, ideal=50
reorder = InventoryDomainService.calculate_reorder_quantity(item)
# Retorna: 45.0
```

### Validade e Expiração

#### 4. Verificação de Vencimento
- **Método:** `is_expired(item: InventoryItem) -> bool`
- **Regra:** Verifica se data de validade < data atual

#### 5. Vencimento Próximo
- **Método:** `is_near_expiration(item: InventoryItem, days: int = 30) -> bool`
- **Regra Padrão:** Considera vencimento próximo se faltam 30 dias ou menos
- **Customizável:** Aceita quantidade de dias personalizada

**Exemplo:**
```python
# Item com validade em 15 dias
is_near = InventoryDomainService.is_near_expiration(item)  # True (< 30 dias)
is_near_7d = InventoryDomainService.is_near_expiration(item, days=7)  # False (> 7 dias)
```

### Movimentação

#### 6. Validação de Saída
- **Método:** `can_perform_output(item: InventoryItem, quantity: float) -> Tuple[bool, str]`
- **Regras:**
  1. Quantidade disponível suficiente
  2. Item não pode estar vencido

**Exemplo:**
```python
can_remove, reason = InventoryDomainService.can_perform_output(item, quantity=10)
if not can_remove:
    raise Exception(reason)  # "Estoque insuficiente" ou "Item vencido"
```

### Cálculos Financeiros

#### 7. Valor Total do Estoque
- **Método:** `calculate_total_value(item: InventoryItem) -> float`
- **Fórmula:** `quantity * unit_cost`

---

## 🏥 Prestadores (Providers)

**Arquivo:** `src/domain/services/provider_service.py`

### Validações de Documentos

#### 1. Validação de CPF
- **Método:** `_validate_cpf(cpf: str) -> bool`
- **Regras:**
  - 11 dígitos numéricos
  - Rejeita CPFs com todos os dígitos iguais
  - Valida dígitos verificadores (algoritmo completo)

**Exemplo:**
```python
# CPF válido: 123.456.789-09
is_valid = ProviderDomainService._validate_cpf("12345678909")
# Retorna: True (dígitos verificadores 09 estão corretos)
```

#### 2. Validação de CNPJ
- **Método:** `_validate_cnpj(cnpj: str) -> bool`
- **Processo:** Idêntico ao descrito em Insurers

#### 3. Validação Genérica de Documento
- **Método:** `validate_document(document: str) -> Tuple[bool, str]`
- **Regra:** Detecta automaticamente se é CPF (11 dígitos) ou CNPJ (14 dígitos)
- **Retorno:** `(é_válido, tipo_documento)`

**Exemplo:**
```python
is_valid, doc_type = ProviderDomainService.validate_document("12345678909")
# Retorna: (True, "CPF")

is_valid, doc_type = ProviderDomainService.validate_document("11222333000181")
# Retorna: (True, "CNPJ")
```

### Credenciais e Qualificações

#### 4. Verificação de Credenciais Válidas
- **Método:** `has_valid_credentials(provider: Provider) -> bool`
- **Regras:**
  - Todas as credenciais devem ter número preenchido
  - Data de validade deve ser futura (se informada)

**Exemplo:**
```python
has_valid = ProviderDomainService.has_valid_credentials(provider)
# Retorna False se alguma credencial estiver vencida
```

### Operações

#### 5. Verificação de Operadora Aceita
- **Método:** `accepts_insurer(provider: Provider, insurer_id: UUID) -> bool`
- **Regra:** Verifica se o ID da operadora está na lista de operadoras aceitas

#### 6. Desativação
- **Método:** `can_be_deactivated(provider: Provider) -> Tuple[bool, str]`
- **Regras:**
  - Pode desativar se não houver agendamentos futuros
  - Verifica na lista de agendamentos (quando implementado)

### Disponibilidade

#### 7. Cálculo de Disponibilidade
- **Método:** `calculate_availability(provider: Provider) -> float`
- **Regras:**
  - Base: 100% se houver horários de trabalho definidos
  - -10% por credencial vencida
  - +5% por especialidade adicional
  - -20% se não aceitar operadoras
  - Mínimo: 0%, Máximo: 100%

**Exemplo:**
```python
availability = ProviderDomainService.calculate_availability(provider)
# Prestador com 2 credenciais vencidas, 3 especialidades, aceita operadoras
# Cálculo: 100 - 20 (2 credenciais) + 10 (2 especialidades extras) = 90%
```

---

## 📊 Relatórios (Reports)

**Arquivo:** `src/domain/services/report_service.py`

### Validações

#### 1. Validação de Criação
- **Método:** `validate_for_creation(report_type: ReportType, start_date: date, end_date: date) -> List[str]`
- **Regras:**
  - Data inicial obrigatória
  - Data final obrigatória
  - Data final ≥ data inicial
  - Intervalo máximo de 5 anos (1825 dias)

**Exemplo:**
```python
errors = ReportDomainService.validate_for_creation(
    report_type=ReportType.PATIENTS,
    start_date=date(2020, 1, 1),
    end_date=date(2026, 1, 1),  # Mais de 5 anos
)
# Retorna: ["Intervalo máximo permitido é de 5 anos"]
```

### Períodos Padrão

#### 2. Intervalos de Data por Período
- **Método:** `get_default_date_range(period: ReportPeriod) -> Tuple[date, date]`
- **Regras:**
  - `DAILY`: Hoje
  - `WEEKLY`: Últimos 7 dias
  - `MONTHLY`: Mês atual
  - `QUARTERLY`: Últimos 3 meses
  - `YEARLY`: Ano atual
  - `CUSTOM`: Requer datas manuais

**Exemplo:**
```python
start, end = ReportDomainService.get_default_date_range(ReportPeriod.MONTHLY)
# Se hoje é 15/01/2024
# Retorna: (date(2024, 1, 1), date(2024, 1, 31))
```

### Estimativas

#### 3. Tempo de Geração
- **Método:** `estimate_generation_time(report_type: ReportType, start_date: date, end_date: date) -> int`
- **Regras Base:**
  - Pacientes: 2 segundos/mês
  - Financeiro: 3 segundos/mês
  - Estatístico: 5 segundos/mês
  - Operacional: 1 segundo/mês
- **Fórmula:** `tempo_base * número_de_meses`
- **Mínimo:** 5 segundos

**Exemplo:**
```python
# Relatório de pacientes para 6 meses
seconds = ReportDomainService.estimate_generation_time(
    ReportType.PATIENTS,
    date(2024, 1, 1),
    date(2024, 6, 30),
)
# Retorna: 12 segundos (2 * 6 meses)
```

### Regeneração

#### 4. Permissão de Regenerar
- **Método:** `can_regenerate(report: Report) -> Tuple[bool, str]`
- **Regras:**
  - Permite se status = `FAILED`
  - Permite se status = `COMPLETED` (mas com aviso)
  - Não permite se `PENDING` ou `PROCESSING`

---

## 👥 Pacientes (Patients)

**Arquivo:** `src/domain/services/patient_service.py`

### Validações

#### 1. Validação de CPF
- **Método:** `validate_cpf(cpf: str) -> bool`
- **Processo:** Idêntico ao descrito em Providers
- **Uso:** Validar documento do paciente

### Cálculos de Idade

#### 2. Cálculo de Idade
- **Método:** `calculate_age(birth_date: date, reference_date: Optional[date] = None) -> int`
- **Regras:**
  - Usa data atual se `reference_date` não fornecida
  - Considera mês e dia para cálculo preciso
  - Retorna idade em anos completos

**Exemplo:**
```python
# Paciente nascido em 15/03/2000, hoje é 10/01/2024
age = PatientDomainService.calculate_age(date(2000, 3, 15))
# Retorna: 23 (ainda não fez aniversário em 2024)

age_at_date = PatientDomainService.calculate_age(
    date(2000, 3, 15),
    reference_date=date(2024, 3, 20)
)
# Retorna: 24 (já fez aniversário em 20/03/2024)
```

### Classificações

#### 3. Paciente Pediátrico
- **Método:** `is_pediatric(patient: Patient) -> bool`
- **Regra:** Idade < 18 anos

#### 4. Paciente Idoso
- **Método:** `is_elderly(patient: Patient) -> bool`
- **Regra:** Idade ≥ 65 anos

#### 5. Nível de Risco
- **Método:** `get_risk_level(patient: Patient) -> str`
- **Regras:**
  - `HIGH`: Idade ≥ 65 ou tem doenças crônicas
  - `MEDIUM`: 45 ≤ idade < 65
  - `LOW`: Idade < 45 e sem doenças crônicas

**Exemplo:**
```python
risk = PatientDomainService.get_risk_level(patient)
# Paciente de 70 anos: "HIGH"
# Paciente de 50 anos: "MEDIUM"
# Paciente de 30 anos: "LOW"
```

### Acompanhamento

#### 6. Necessidade de Acompanhante
- **Método:** `requires_companion(patient: Patient) -> Tuple[bool, str]`
- **Regras:**
  - Obrigatório se idade < 18 (menor de idade)
  - Obrigatório se idade ≥ 65 (idoso)
  - Opcional para idades entre 18 e 64

**Exemplo:**
```python
requires, reason = PatientDomainService.requires_companion(patient)
# Paciente de 15 anos: (True, "Paciente menor de idade")
# Paciente de 70 anos: (True, "Paciente idoso requer acompanhante")
# Paciente de 35 anos: (False, "Não requer acompanhante")
```

---

## 🎯 Uso nos Use Cases

### Padrão de Integração

Todos os Use Cases seguem o mesmo padrão para usar os Domain Services:

```python
class CreateXxxUseCase:
    """Use Case para criar entidade."""
    
    def __init__(self, repository: XxxRepository) -> None:
        self._repository = repository
    
    async def execute(self, input_dto: CreateXxxInput) -> CreateXxxOutput:
        # 1. Validar usando Domain Service
        errors = XxxDomainService.validate_for_creation(...)
        if errors:
            raise ApplicationException("; ".join(errors))
        
        # 2. Validar documento (se aplicável)
        if not XxxDomainService.validate_cpf(input_dto.cpf):
            raise ApplicationException("CPF inválido")
        
        # 3. Verificar duplicatas
        existing = await self._repository.get_by_document(...)
        if existing:
            raise ApplicationException("Já existe")
        
        # 4. Criar entidade
        entity = Xxx.create(...)
        
        # 5. Persistir
        created = await self._repository.create(entity)
        
        return CreateXxxOutput(...)
```

### Benefícios da Centralização

1. **Consistência:** Mesmas regras aplicadas em todos os lugares
2. **Manutenibilidade:** Alterar regra em um único lugar
3. **Testabilidade:** Testar regras independentemente
4. **Reutilização:** Domain Services usados em múltiplos Use Cases
5. **Separação de Responsabilidades:** Lógica de negócio separada de infraestrutura

---

## 📝 Notas de Implementação

### Validações de Documentos

Os algoritmos de validação de CPF e CNPJ implementam o cálculo completo dos dígitos verificadores:

- **CPF:** Mod 11 com pesos de 10-2 e 11-2
- **CNPJ:** Mod 11 com pesos de 5-2, 6-2

### Mensagens de Erro

Todas as mensagens de erro estão em português brasileiro para facilitar a experiência do usuário final.

### Extensibilidade

Para adicionar novas regras:

1. Adicione método no Domain Service apropriado
2. Use o método no Use Case correspondente
3. Adicione testes unitários
4. Documente neste arquivo

### Testes

Cada Domain Service deve ter testes unitários cobrindo:
- Casos válidos
- Casos inválidos
- Casos limites (edge cases)
- Validações de documentos com dígitos verificadores

---

## 🔄 Migração Frontend → Backend

### Status da Migração

✅ **Completo:**
- Todas as validações de documentos (CPF, CNPJ)
- Todas as regras de negócio dos módulos principais
- Cálculos de idade e classificações
- Validações de períodos e datas
- Regras de desativação e status

### Frontend Atual

O frontend pode agora:
1. Remover validações complexas (CPF, CNPJ)
2. Delegar verificações de negócio para API
3. Focar em validações de UI (campos obrigatórios, formatos básicos)
4. Exibir mensagens de erro retornadas pelo backend

### Exemplo de Chamada do Frontend

```typescript
// Antes: Validação no frontend
if (!validateCPF(cpf)) {
  showError("CPF inválido");
  return;
}

// Depois: Delegação para backend
try {
  await api.post('/patients', { cpf, ... });
} catch (error) {
  showError(error.message); // "CPF inválido (dígitos verificadores incorretos)"
}
```

---

## 📚 Referências

- Clean Architecture (Robert C. Martin)
- Domain-Driven Design (Eric Evans)
- Receita Federal do Brasil (Algoritmos de CPF/CNPJ)
- ANS - Agência Nacional de Saúde Suplementar

---

**Última atualização:** Janeiro 2024
**Versão:** 1.0.0
