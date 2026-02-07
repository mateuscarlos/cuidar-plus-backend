.PHONY: help build up up-dev down down-v logs logs-db shell shell-db test migrate migrate-create clean rebuild pgadmin

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build dos containers (produção)
	docker-compose build

up: ## Inicia os containers em background (produção)
	docker-compose up -d

up-dev: ## Inicia containers em modo desenvolvimento com hot reload
	docker-compose -f docker-compose.dev.yml up --build

up-dev-d: ## Inicia containers dev em background
	docker-compose -f docker-compose.dev.yml up -d --build

down: ## Para e remove os containers
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

down-v: ## Para e remove containers e volumes (APAGA DADOS!)
	docker-compose down -v
	docker-compose -f docker-compose.dev.yml down -v

logs: ## Mostra logs da API
	docker-compose logs -f backend

logs-db: ## Mostra logs do banco
	docker-compose logs -f db

shell: ## Abre shell no container da API
	docker-compose exec backend /bin/bash

shell-db: ## Abre psql no container do banco
	docker-compose exec db psql -U postgres -d cuidar_plus

test: ## Roda os testes no container
	docker-compose exec backend pytest -v

migrate: ## Roda as migrations do Alembic
	docker-compose exec backend alembic upgrade head

migrate-create: ## Cria nova migration (uso: make migrate-create MSG="descricao")
	docker-compose exec backend alembic revision --autogenerate -m "$(MSG)"

init-db: ## Inicializa o banco com dados de teste
	docker-compose exec backend python -m scripts.init_db

clean: ## Remove containers, volumes e imagens não utilizadas
	docker-compose down -v --rmi local
	docker-compose -f docker-compose.dev.yml down -v --rmi local
	docker system prune -f

rebuild: ## Reconstrói os containers do zero
	docker-compose down -v
	docker-compose build --no-cache
	docker-compose up -d

pgadmin: ## Inicia PgAdmin para gerenciamento do banco
	docker-compose --profile tools up -d pgadmin
