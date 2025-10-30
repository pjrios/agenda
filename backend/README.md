# Agenda Backend

This FastAPI service powers the Agenda platform. It exposes REST and GraphQL APIs for managing class structures, academic calendars, lesson plans, and instructional resources. SQLAlchemy models are backed by Alembic migrations, and semantic search is enabled through a lightweight TF-IDF vector store.

## Features

- CRUD endpoints for levels, subjects, groups, schedules, trimesters, sessions, materials, rubrics, and calendar artifacts
- Plan duplication workflows with per-group overrides
- Semantic search across lesson materials and resources
- Background jobs to refresh vector embeddings
- GraphQL endpoint for consuming class data in rich clients

## Getting started

```bash
cd backend
pip install -e .
uvicorn app.main:app --reload
```

### Database migrations

Alembic is configured under `app/migrations`. To apply migrations locally:

```bash
alembic upgrade head
```

### Running tests

```bash
pytest
```
