-- Script de inicialização do PostgreSQL
-- Executado automaticamente apenas na primeira criação do volume

-- Extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Configurações de log para desenvolvimento
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_duration = 'on';

SELECT pg_reload_conf();
