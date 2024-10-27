from typing import List, Optional, Dict
from pydantic import BaseModel
from uuid import UUID

class DocumentOutput(Dict[str, str]):
    """Type alias for document output dictionary"""
    pass

class Pages(Dict[int, str]):
    """Type alias for pages dictionary"""
    pass

class RAGQuery(BaseModel):
    question: str
    document_id: str
    max_chunks: Optional[int] = 5

class RAGResponse(BaseModel):
    answer: str
    source_pages: List[int]

class ChunkData(BaseModel):
    content: str
    page_number: int
    embedding: Optional[List[float]] = None

class ChunksResponse(BaseModel):
    document_id: UUID
    chunks: List[ChunkData]