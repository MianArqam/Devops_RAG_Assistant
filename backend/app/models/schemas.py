from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=3)


class LogAnalysisRequest(BaseModel):
    log: str = Field(..., min_length=3)


class Source(BaseModel):
    source: str
    score: float
    text: str


class RagResponse(BaseModel):
    answer: str
    sources: list[Source]


class UploadResponse(BaseModel):
    filename: str
    chunks_added: int
    message: str
