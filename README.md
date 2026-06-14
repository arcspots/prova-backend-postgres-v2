# Prova Técnica – Desenvolvedor Back-end (IA) v2.0

## Descrição do Projeto

Esta é a versão 2.0 da solução da prova técnica para Desenvolvedor Back-end com foco em Inteligência Artificial.

Nesta versão, o projeto foi evoluído de SQLite para PostgreSQL, utilizando uma arquitetura com múltiplos containers Docker para simular um ambiente mais próximo de produção.

A aplicação consiste em uma API RESTful desenvolvida em Python com FastAPI, oferecendo:

* CRUD completo de usuários
* Autenticação via JWT
* Integração com modelo de Machine Learning
* Persistência com PostgreSQL
* Containerização com Docker Compose

---

## Diferença entre v1 e v2

### Versão 1

* SQLite (banco local em arquivo)
* Single container
* Ideal para prototipagem rápida

### Versão 2 (Atual)

* PostgreSQL (banco real)
* Multi-container Docker
* Arquitetura mais próxima de produção

---

## Tecnologias Utilizadas

* Python 3.11
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT (python-jose)
* Scikit-Learn
* Joblib
* Docker
* Docker Compose
* Jupyter Notebook

---

## Arquitetura

Cliente (Swagger / Frontend)
↓
FastAPI Container
↓
SQLAlchemy ORM
↓
PostgreSQL Container

---

## Estrutura do Projeto

```bash
Prova_Backend_Alyson_Ribeiro_v2.0/
│
├── app/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── ml_model.pkl
│
├── notebooks/
│   └── prova.ipynb
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Funcionalidades

### Autenticação JWT

* POST /login

Gera token JWT para acessar endpoints protegidos.

Credenciais de teste:

```json
{
  "username": "admin",
  "password": "123456"
}
```

---

### CRUD de Usuários

Endpoints:

* POST /users
* GET /users
* GET /users/{id}
* PUT /users/{id}
* DELETE /users/{id}

Todos protegidos por JWT.

---

### Predição com IA

Endpoint:

* POST /predict

Recebe um valor numérico e utiliza o modelo treinado para gerar uma predição.

Exemplo:

```json
{
  "value": 15
}
```

Resposta:

```json
{
  "prediction": 30
}
```

---

## Executando Localmente (Sem Docker)

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar API:

```bash
uvicorn app.main:app --reload
```

Abrir documentação:

```bash
http://127.0.0.1:8000/docs
```

---

## Executando com Docker

Subir containers:

```bash
docker compose up --build
```

Containers criados:

* backend_api
* postgres_db

Acessar API:

```bash
http://localhost:8000/docs
```

---

## Banco de Dados

Nesta versão, o banco utilizado é PostgreSQL em container dedicado.

Configuração da conexão:

* Host: db
* Porta: 5432
* Database: prova_backend
* User: postgres

---

## Observações Técnicas

A migração de SQLite para PostgreSQL exigiu principalmente:

* alteração da connection string no SQLAlchemy
* remoção de configurações específicas do SQLite
* adição do driver psycopg2
* criação de container dedicado para banco

Essa mudança permitiu simular melhor uma arquitetura real de backend em produção.
