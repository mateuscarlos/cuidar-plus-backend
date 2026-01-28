# API Examples - Cuidar Plus Backend

Exemplos práticos de uso da API com curl, Python e JavaScript.

---

## 🔐 1. Autenticação

### Login

**curl:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@cuidarplus.com",
    "password": "admin123"
  }'
```

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:5000/api/v1/auth/login",
    json={
        "email": "admin@cuidarplus.com",
        "password": "admin123"
    }
)

data = response.json()
access_token = data["access_token"]
refresh_token = data["refresh_token"]
```

**JavaScript:**
```javascript
const response = await fetch('http://localhost:5000/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'admin@cuidarplus.com',
    password: 'admin123'
  })
});

const { access_token, refresh_token } = await response.json();
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

---

### Refresh Token

**curl:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "seu_refresh_token_aqui"
  }'
```

---

## 👤 2. Gerenciamento de Usuários

### Criar Usuário

**curl:**
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "caregiver@example.com",
    "password": "senha123",
    "full_name": "João Silva",
    "role": "caregiver"
  }'
```

**Python:**
```python
response = requests.post(
    "http://localhost:5000/api/v1/users/",
    json={
        "email": "caregiver@example.com",
        "password": "senha123",
        "full_name": "João Silva",
        "role": "caregiver"
    }
)

user = response.json()
user_id = user["id"]
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "caregiver@example.com",
  "full_name": "João Silva",
  "role": "caregiver",
  "is_active": true
}
```

---

### Buscar Usuário (requer autenticação)

**curl:**
```bash
curl http://localhost:5000/api/v1/users/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer seu_access_token_aqui"
```

**Python:**
```python
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(
    f"http://localhost:5000/api/v1/users/{user_id}",
    headers=headers
)
user = response.json()
```

**JavaScript:**
```javascript
const response = await fetch(
  `http://localhost:5000/api/v1/users/${userId}`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);
const user = await response.json();
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "caregiver@example.com",
  "full_name": "João Silva",
  "role": "caregiver",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "last_login": "2024-01-26T14:20:00"
}
```

---

## 👴 3. Gerenciamento de Pacientes

### Criar Paciente

**curl:**
```bash
curl -X POST http://localhost:5000/api/v1/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer seu_access_token_aqui" \
  -d '{
    "caregiver_id": "550e8400-e29b-41d4-a716-446655440000",
    "full_name": "Maria Silva",
    "cpf": "111.444.777-35",
    "date_of_birth": "1950-05-15",
    "gender": "F",
    "address": "Rua das Flores, 123, São Paulo - SP",
    "phone": "(11) 98765-4321",
    "emergency_contact": "João Silva",
    "emergency_phone": "(11) 91234-5678",
    "medical_conditions": "Hipertensão arterial, Diabetes tipo 2",
    "allergies": "Penicilina",
    "observations": "Paciente lúcida e orientada. Precisa de auxílio para locomoção."
  }'
```

**Python:**
```python
headers = {"Authorization": f"Bearer {access_token}"}
patient_data = {
    "caregiver_id": user_id,
    "full_name": "Maria Silva",
    "cpf": "111.444.777-35",
    "date_of_birth": "1950-05-15",
    "gender": "F",
    "address": "Rua das Flores, 123, São Paulo - SP",
    "phone": "(11) 98765-4321",
    "emergency_contact": "João Silva",
    "emergency_phone": "(11) 91234-5678",
    "medical_conditions": "Hipertensão arterial, Diabetes tipo 2",
    "allergies": "Penicilina",
    "observations": "Paciente lúcida e orientada."
}

response = requests.post(
    "http://localhost:5000/api/v1/patients/",
    headers=headers,
    json=patient_data
)

patient = response.json()
patient_id = patient["id"]
```

**Response:**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "caregiver_id": "550e8400-e29b-41d4-a716-446655440000",
  "full_name": "Maria Silva",
  "cpf": "111.444.777-35",
  "age": 74,
  "gender": "F"
}
```

---

### Listar Pacientes por Cuidador

**curl:**
```bash
curl http://localhost:5000/api/v1/patients/caregiver/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer seu_access_token_aqui"
```

**Python:**
```python
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(
    f"http://localhost:5000/api/v1/patients/caregiver/{user_id}",
    headers=headers
)
patients = response.json()
```

**Response:**
```json
{
  "patients": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "full_name": "Maria Silva",
      "age": 74,
      "gender": "F",
      "is_active": true
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440002",
      "full_name": "José Santos",
      "age": 80,
      "gender": "M",
      "is_active": true
    }
  ],
  "total": 2
}
```

---

## 💊 4. Gerenciamento de Medicamentos

### Criar Medicamento

**curl:**
```bash
curl -X POST http://localhost:5000/api/v1/medications/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer seu_access_token_aqui" \
  -d '{
    "patient_id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Losartana",
    "dosage": "50mg",
    "frequency": "daily",
    "schedule_times": ["08:00:00", "20:00:00"],
    "start_date": "2024-01-26T00:00:00",
    "end_date": null,
    "instructions": "Tomar após o café da manhã e jantar"
  }'
```

**Python:**
```python
from datetime import datetime, time

headers = {"Authorization": f"Bearer {access_token}"}
medication_data = {
    "patient_id": patient_id,
    "name": "Losartana",
    "dosage": "50mg",
    "frequency": "daily",
    "schedule_times": ["08:00:00", "20:00:00"],
    "start_date": datetime.now().isoformat(),
    "end_date": None,
    "instructions": "Tomar após o café da manhã e jantar"
}

response = requests.post(
    "http://localhost:5000/api/v1/medications/",
    headers=headers,
    json=medication_data
)

medication = response.json()
```

---

## 🏥 5. Gerenciamento de Consultas

### Criar Consulta

**Python:**
```python
from datetime import datetime, timedelta

headers = {"Authorization": f"Bearer {access_token}"}
appointment_data = {
    "patient_id": patient_id,
    "title": "Consulta Cardiologista",
    "description": "Consulta de rotina",
    "appointment_date": (datetime.now() + timedelta(days=7)).isoformat(),
    "duration_minutes": 60,
    "location": "Clínica São Paulo - Rua Augusta, 500",
    "doctor_name": "Dr. Carlos Santos",
    "specialty": "Cardiologia"
}

response = requests.post(
    "http://localhost:5000/api/v1/appointments/",
    headers=headers,
    json=appointment_data
)
```

---

## 🔍 6. Health Check

**curl:**
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "cuidar-plus-backend",
  "version": "v1"
}
```

---

## ⚠️ 7. Tratamento de Erros

### Erro de Autenticação (401)
```json
{
  "error": "Invalid email or password",
  "code": "INVALID_CREDENTIALS"
}
```

### Erro de Validação (400)
```json
{
  "error": "Email and password are required",
  "code": "VALIDATION_ERROR"
}
```

### Recurso Não Encontrado (404)
```json
{
  "error": "User with ID xxx not found",
  "code": "USER_NOT_FOUND"
}
```

### Token Expirado (401)
```json
{
  "error": "Token has expired",
  "code": "TOKEN_EXPIRED"
}
```

### Erro Interno (500)
```json
{
  "error": "Internal server error",
  "code": "INTERNAL_ERROR"
}
```

---

## 📦 8. Cliente Python Completo

```python
import requests
from typing import Optional

class CuidarPlusClient:
    """Cliente Python para API Cuidar Plus."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
    
    def login(self, email: str, password: str) -> dict:
        """Autenticar usuário."""
        response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        
        return data
    
    def _get_headers(self) -> dict:
        """Retorna headers com autenticação."""
        if not self.access_token:
            raise ValueError("Not authenticated. Call login() first.")
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def create_user(self, email: str, password: str, 
                    full_name: str, role: str) -> dict:
        """Criar novo usuário."""
        response = requests.post(
            f"{self.base_url}/api/v1/users/",
            json={
                "email": email,
                "password": password,
                "full_name": full_name,
                "role": role
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_user(self, user_id: str) -> dict:
        """Buscar usuário por ID."""
        response = requests.get(
            f"{self.base_url}/api/v1/users/{user_id}",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_patient(self, **patient_data) -> dict:
        """Criar novo paciente."""
        response = requests.post(
            f"{self.base_url}/api/v1/patients/",
            headers=self._get_headers(),
            json=patient_data
        )
        response.raise_for_status()
        return response.json()
    
    def list_patients(self, caregiver_id: str) -> dict:
        """Listar pacientes de um cuidador."""
        response = requests.get(
            f"{self.base_url}/api/v1/patients/caregiver/{caregiver_id}",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()


# Exemplo de uso:
if __name__ == "__main__":
    client = CuidarPlusClient()
    
    # Login
    auth = client.login("admin@cuidarplus.com", "admin123")
    print(f"Logged in! Token: {auth['access_token'][:20]}...")
    
    # Criar usuário
    user = client.create_user(
        email="teste@example.com",
        password="senha123",
        full_name="Teste User",
        role="caregiver"
    )
    print(f"User created: {user['id']}")
    
    # Buscar usuário
    user_details = client.get_user(user['id'])
    print(f"User details: {user_details}")
```

---

## 🌐 9. Cliente JavaScript/TypeScript

```typescript
class CuidarPlusClient {
  private baseUrl: string;
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  constructor(baseUrl: string = 'http://localhost:5000') {
    this.baseUrl = baseUrl;
  }

  async login(email: string, password: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data = await response.json();
    this.accessToken = data.access_token;
    this.refreshToken = data.refresh_token;

    return data;
  }

  private getHeaders(): HeadersInit {
    if (!this.accessToken) {
      throw new Error('Not authenticated');
    }
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.accessToken}`
    };
  }

  async createUser(userData: any): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/v1/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      throw new Error('Failed to create user');
    }

    return response.json();
  }

  async getUser(userId: string): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/api/v1/users/${userId}`,
      { headers: this.getHeaders() }
    );

    if (!response.ok) {
      throw new Error('Failed to get user');
    }

    return response.json();
  }

  async createPatient(patientData: any): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/v1/patients/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(patientData)
    });

    if (!response.ok) {
      throw new Error('Failed to create patient');
    }

    return response.json();
  }

  async listPatients(caregiverId: string): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/api/v1/patients/caregiver/${caregiverId}`,
      { headers: this.getHeaders() }
    );

    if (!response.ok) {
      throw new Error('Failed to list patients');
    }

    return response.json();
  }
}

// Uso:
const client = new CuidarPlusClient();

(async () => {
  await client.login('admin@cuidarplus.com', 'admin123');
  
  const user = await client.createUser({
    email: 'teste@example.com',
    password: 'senha123',
    full_name: 'Teste User',
    role: 'caregiver'
  });
  
  console.log('User created:', user);
})();
```

---

**Versão**: 1.0  
**Data**: Janeiro 2026
