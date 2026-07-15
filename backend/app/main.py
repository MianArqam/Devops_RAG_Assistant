from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.rag.vector_store import vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    if vector_store.count() == 0:
        vector_store.ingest_knowledge_base()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health() -> dict[str, str | int]:
    return {
        "status": "ok",
        "indexed_chunks": vector_store.count(),
        "llm_provider": settings.llm_provider,
    }
