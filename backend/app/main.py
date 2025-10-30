from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine
from strawberry.fastapi import GraphQLRouter

from .api.graphql import create_schema
from .api.routes import router as api_router
from .database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app(sql_engine: AsyncEngine = engine) -> FastAPI:
    app = FastAPI(title="Agenda Platform", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.include_router(api_router, prefix="/api")

    graphql_router = GraphQLRouter(create_schema())
    app.include_router(graphql_router, prefix="/graphql")

    return app


app = create_app()
