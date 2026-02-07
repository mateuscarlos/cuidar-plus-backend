#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script de gerenciamento Docker para Cuidar Plus Backend (Windows)
.DESCRIPTION
    Substitui o Makefile para uso no PowerShell/Windows.
    Uso: .\docker.ps1 <comando>
.EXAMPLE
    .\docker.ps1 up-dev
    .\docker.ps1 logs
    .\docker.ps1 shell
#>

param(
    [Parameter(Position = 0)]
    [ValidateSet(
        "help", "build", "up", "up-dev", "up-dev-d", "down", "down-v",
        "logs", "logs-db", "shell", "shell-db", "test",
        "migrate", "migrate-create", "init-db",
        "clean", "rebuild", "pgadmin", "status"
    )]
    [string]$Command = "help",

    [Parameter(Position = 1)]
    [string]$Message = ""
)

function Show-Help {
    Write-Host ""
    Write-Host "  Cuidar Plus Backend - Docker Commands" -ForegroundColor Cyan
    Write-Host "  ======================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  build          " -NoNewline -ForegroundColor Yellow; Write-Host "Build dos containers (producao)"
    Write-Host "  up             " -NoNewline -ForegroundColor Yellow; Write-Host "Inicia containers em background (producao)"
    Write-Host "  up-dev         " -NoNewline -ForegroundColor Yellow; Write-Host "Inicia containers em modo dev com hot reload"
    Write-Host "  up-dev-d       " -NoNewline -ForegroundColor Yellow; Write-Host "Inicia containers dev em background"
    Write-Host "  down           " -NoNewline -ForegroundColor Yellow; Write-Host "Para e remove os containers"
    Write-Host "  down-v         " -NoNewline -ForegroundColor Yellow; Write-Host "Para e remove containers e volumes (APAGA DADOS!)"
    Write-Host "  logs           " -NoNewline -ForegroundColor Yellow; Write-Host "Mostra logs da API"
    Write-Host "  logs-db        " -NoNewline -ForegroundColor Yellow; Write-Host "Mostra logs do banco"
    Write-Host "  shell          " -NoNewline -ForegroundColor Yellow; Write-Host "Abre shell no container da API"
    Write-Host "  shell-db       " -NoNewline -ForegroundColor Yellow; Write-Host "Abre psql no container do banco"
    Write-Host "  test           " -NoNewline -ForegroundColor Yellow; Write-Host "Roda os testes no container"
    Write-Host "  migrate        " -NoNewline -ForegroundColor Yellow; Write-Host "Roda as migrations do Alembic"
    Write-Host "  migrate-create " -NoNewline -ForegroundColor Yellow; Write-Host 'Cria nova migration (uso: .\docker.ps1 migrate-create "descricao")'
    Write-Host "  init-db        " -NoNewline -ForegroundColor Yellow; Write-Host "Inicializa o banco com dados de teste"
    Write-Host "  clean          " -NoNewline -ForegroundColor Yellow; Write-Host "Remove containers, volumes e imagens"
    Write-Host "  rebuild        " -NoNewline -ForegroundColor Yellow; Write-Host "Reconstroi do zero"
    Write-Host "  pgadmin        " -NoNewline -ForegroundColor Yellow; Write-Host "Inicia PgAdmin"
    Write-Host "  status         " -NoNewline -ForegroundColor Yellow; Write-Host "Mostra status dos containers"
    Write-Host ""
}

switch ($Command) {
    "help"           { Show-Help }
    "build"          { docker-compose build }
    "up"             { docker-compose up -d }
    "up-dev"         { docker-compose -f docker-compose.dev.yml up --build }
    "up-dev-d"       { docker-compose -f docker-compose.dev.yml up -d --build }
    "down"           { docker-compose down; docker-compose -f docker-compose.dev.yml down }
    "down-v"         { docker-compose down -v; docker-compose -f docker-compose.dev.yml down -v }
    "logs"           { docker-compose logs -f backend }
    "logs-db"        { docker-compose logs -f db }
    "shell"          { docker-compose exec backend /bin/bash }
    "shell-db"       { docker-compose exec db psql -U postgres -d cuidar_plus }
    "test"           { docker-compose exec backend pytest -v }
    "migrate"        { docker-compose exec backend alembic upgrade head }
    "migrate-create" {
        if ([string]::IsNullOrEmpty($Message)) {
            Write-Host "Erro: informe a descricao da migration" -ForegroundColor Red
            Write-Host 'Uso: .\docker.ps1 migrate-create "descricao da migration"' -ForegroundColor Yellow
            exit 1
        }
        docker-compose exec backend alembic revision --autogenerate -m $Message
    }
    "init-db"        { docker-compose exec backend python -m scripts.init_db }
    "clean"          {
        docker-compose down -v --rmi local
        docker-compose -f docker-compose.dev.yml down -v --rmi local
        docker system prune -f
    }
    "rebuild"        {
        docker-compose down -v
        docker-compose build --no-cache
        docker-compose up -d
    }
    "pgadmin"        { docker-compose --profile tools up -d pgadmin }
    "status"         { docker-compose ps; docker-compose -f docker-compose.dev.yml ps }
}
