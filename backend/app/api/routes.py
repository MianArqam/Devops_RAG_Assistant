from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.models.schemas import ChatRequest, LogAnalysisRequest, RagResponse, Source, UploadResponse
from app.rag.document_loader import SUPPORTED_EXTENSIONS, read_document
from app.rag.llm import generate_answer
from app.rag.vector_store import vector_store

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    original_name = file.filename or "document.txt"
    extension = Path(original_name).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Upload a PDF, TXT, or MD file.")

    upload_dir = settings.resolved_knowledge_base_dir / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    safe_name = f"{uuid4().hex}_{Path(original_name).name}"
    destination = upload_dir / safe_name
    destination.write_bytes(await file.read())

    text = read_document(destination)
    chunks_added = vector_store.add_document(text, f"uploads/{safe_name}")
    return UploadResponse(
        filename=original_name,
        chunks_added=chunks_added,
        message="Document uploaded and indexed.",
    )


@router.post("/chat", response_model=RagResponse)
async def chat(request: ChatRequest) -> RagResponse:
    matches = vector_store.search(request.query)
    context = format_context(matches)
    answer = await generate_answer(request.query, context)
    return RagResponse(answer=answer, sources=[Source(**match) for match in matches])


@router.post("/analyze-log", response_model=RagResponse)
async def analyze_log(request: LogAnalysisRequest) -> RagResponse:
    query = f"Analyze this DevOps log and suggest a fix:\n{request.log}"
    matches = vector_store.search(query)
    context = format_context(matches)
    answer = await generate_answer(query, context)
    return RagResponse(answer=answer, sources=[Source(**match) for match in matches])


def format_context(matches: list[dict[str, str | float]]) -> str:
    sections = []
    for match in matches:
        sections.append(
            f"Source: {match['source']}\n"
            f"Similarity: {match['score']:.3f}\n"
            f"{match['text']}"
        )
    return "\n\n---\n\n".join(sections)
