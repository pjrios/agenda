# Agenda Platform

This repository contains a full-stack scaffold for an academic agenda platform composed of a FastAPI backend and a React frontend.

## Structure

- `backend/`: FastAPI service with SQLAlchemy models, Alembic migrations, REST and GraphQL APIs, and a semantic search subsystem.
- `frontend/`: React + Vite application providing calendar views, trimester timelines, resource planning, and rubric management interfaces.

## Getting started

### Backend

```bash
cd backend
pip install -e .
uvicorn app.main:app --reload
```

Apply database migrations with Alembic:

```bash
alembic upgrade head
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The development server assumes the backend is running on `http://localhost:8000`.
