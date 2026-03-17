# ComunitBooks

Plataforma de compartilhamento de livros entre membros de uma comunidade. A ideia é simples: emprestar e trocar livros como se fossem amigos — sem burocracia, mas com controle suficiente para evitar abusos.

---

## Stack

- **Backend:** Django 5.2 + Python 3.12
- **Banco de dados:** PostgreSQL 16 (produção) / SQLite (desenvolvimento)
- **Cache / Fila:** Redis 7 + Celery
- **Servidor:** Gunicorn + Nginx
- **Deploy:** Docker + Docker Compose
- **E-mail:** Resend (produção) / arquivo local (desenvolvimento)

---

## Apps

| App | Responsabilidade |
|---|---|
| `usuarios` | Usuário customizado (login por e-mail), perfil, endereço, pontuação |
| `books` | Catálogo de livros, categorias, busca e filtros |
| `orders` | Solicitações de empréstimo (etapa anterior ao Loan) |
| `loans` | Ciclo de vida do empréstimo, renovações, atrasos |
| `core` | Homepage com estatísticas gerais |

---

## Regras de negócio principais

- Período padrão de empréstimo: **14 dias**, com **1 renovação** permitida (+7 dias)
- Máximo de **3 empréstimos simultâneos** por usuário
- Usuários com atraso superior a 5 dias ficam bloqueados
- Sistema de reputação:
  - `+2` por livro doado
  - `+1` por devolução antecipada
  - `-5` por atraso
- Tarefas agendadas via Celery Beat (a cada minuto):
  - Marcação automática de empréstimos em atraso
  - Notificações de vencimento próximo

---

## Configuração

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto. Veja `.env.local` como referência:

```env
SECRET_KEY="sua-secret-key"
DJANGO_SETTINGS_MODULE=config.settings.dev
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

---

## Rodando o projeto

### Com Docker (recomendado)

```bash
# Produção
docker-compose up -d

# Desenvolvimento
docker-compose -f docker-compose.dev.yml up -d
```

Serviços iniciados: `web`, `db`, `redis`, `celery_worker`, `celery_beat`, `nginx`.

### Localmente (sem Docker)

```bash
pip install -r requirements/base.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Comandos úteis

```bash
# Aplicar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Iniciar worker Celery
celery -A config worker -l info

# Iniciar Celery Beat (tarefas agendadas)
celery -A config beat -l info
```

---

## Modelos principais

```
CustomUser ──< Book (owner)
CustomUser ──< Loan (borrower / owner)
CustomUser ──< Order (borrower / owner)
CustomUser ─O2O─ Address

Book ──< Loan
Book ──< Order
Book >──< Category
```

**Status do Loan:** `APPROVED → ON_ROUTE → ACTIVE → IN_RETURN → COMPLETED / OVERDUE / CANCELLED`

**Status do Order:** `SUBMITTED → APPROVED / DENIED / CANCELLED`

---

## Painel de administração

Disponível em `/admin/` após criar um superusuário.
