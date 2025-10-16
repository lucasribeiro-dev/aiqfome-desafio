# Introdução
Aiqfome API Desafio

# Estrutura do Projeto

- Django REST Framework para criação da API.
- PostgreSQL como banco de dados.
- Docker Compose para orquestração dos serviços.
- DRF Spectacular para geração automática de documentação OpenAPI (Swagger).
- Testes unitários integrados com o Django Test Framework.

# Variáveis de Ambiente
O projeto contém um arquivo .env_example.
Renomeie-o para .env e ajuste as variáveis conforme o seu ambiente:

# Rodando Localmente (venv)
1. Install Python 3
2. Create virtual env (python3 -m venv .venv)
3. Activate virtual env (. ./.venv/bin/activate)
4. Install dependencies (pip install -U pip --no-cache && pip install -r requirements.txt)

# Rodando com Docker Compose
```bash
1. docker pull python:3.12-slim
2. docker compose up -d --build
```
# Criar Usuário Admin
Localmente
```bash
python manage.py shell -c "from clients.models import User; User.objects.create_user(email='admin@example.com', username='admin@example.com', password='senha123', is_staff=True)"
```
Dentro do container Docker:
```bash
docker compose exec web python manage.py shell -c "from clients.models import User; User.objects.create_user(email='admin@example.com', username='admin@example.com', password='senha123', is_staff=True)"
```
# Gerar Documentação OpenAPI (Swagger)
Para gerar o arquivo `schema.yml`, execute:
```bash
python manage.py spectacular --file schema.yml
```
# Para rodar os tests
Para gerar o arquivo `schema.yml`, execute:
```bash
python manage.py test
```
