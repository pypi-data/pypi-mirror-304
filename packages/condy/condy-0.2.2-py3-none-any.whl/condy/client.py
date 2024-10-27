import httpx
import logging
from typing import Optional, Union, Dict
from uuid import UUID

from .config import CondyConfig
from .models import (
    DocumentOutput,
    Pages,
    RAGQuery,
    RAGResponse,
    ChunksResponse
)
from .exceptions import NetworkError, TimeoutError, APIError
from .utils import process_markdown, process_text

logger = logging.getLogger(__name__)

class CondyClient:
    """
    Main client for interacting with the Condensation.ai API.
    
    Args:
        api_key (str): Your API key for authentication
        base_url (Optional[str]): Override the default API base URL
        timeout (float): Request timeout in seconds
    """
    
    def __init__(
        self, 
        api_key: str, 
        base_url: Optional[str] = None, 
        timeout: float = 30.0
    ):
        self.config = CondyConfig(api_key)
        if base_url:
            self.config.BASE_URL = base_url
        self.timeout = timeout

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        *,
        json: Optional[dict] = None,
        params: Optional[dict] = None
    ) -> dict:
        """Internal method to make HTTP requests."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                url = f"{self.config.BASE_URL}{endpoint}"
                response = await client.request(
                    method=method,
                    url=url,
                    json=json,
                    params=params,
                    headers=self.config.headers
                )
                
                if not response.is_success:
                    raise APIError(
                        response.status_code,
                        response.json().get('detail', 'Unknown error')
                    )
                    
                return response.json()
                
            except httpx.TimeoutException as e:
                raise TimeoutError("Request timed out") from e
            except httpx.RequestError as e:
                raise NetworkError("Network error occurred") from e

    # Document Processing Methods
    async def fetch_content(self, url: str) -> str:
        """
        Fetch content from a URL.
        
        Args:
            url (str): URL of the content
            
        Returns:
            str: Raw content
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.text
            except httpx.TimeoutException as e:
                logger.error(f"Content fetch timed out: {str(e)}")
                raise TimeoutError("Timeout while fetching content") from e
            except httpx.RequestError as e:
                logger.error(f"Network error during content fetch: {str(e)}")
                raise NetworkError("Network error while fetching content") from e

    async def upload_pages(self, pages: Pages) -> DocumentOutput:
        """
        Upload pages to the Condy API.
        
        Args:
            pages (Pages): Dictionary of page numbers to content
            
        Returns:
            DocumentOutput: Upload result containing document ID
        """
        return await self._make_request(
            "POST",
            "/rag/raginmultipage",
            json={"pages": pages}
        )

    async def process_document(
        self, 
        content: Union[str, Dict[int, str]], 
        content_type: str = "text",
        url: Optional[str] = None,
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> DocumentOutput:
        """
        Process and upload content to the API.
        
        Args:
            content: Either a URL, raw text string, or pre-formatted pages dictionary
            content_type: Type of content ("text", "markdown", or "pages")
            url: Optional URL source of the content
            chunk_size: Size of text chunks when processing raw text
            overlap: Overlap between chunks when processing raw text
            
        Returns:
            DocumentOutput: Upload result containing document ID
        """
        if url:
            content = await self.fetch_content(url)

        if content_type == "pages" and isinstance(content, dict):
            pages_dict = content
        elif content_type == "markdown":
            pages_dict = process_markdown(content)
        else:  # Default to text processing
            pages_dict = process_text(content, chunk_size, overlap)

        return await self.upload_pages(pages_dict)

    # RAG Query Methods
    async def query_rag(
        self, 
        question: str, 
        document_id: str, 
        max_chunks: int = 5
    ) -> RAGResponse:
        """
        Query the RAG system with a question about a specific document.
        
        Args:
            question (str): The question to ask
            document_id (str): ID of the document to query
            max_chunks (int): Maximum number of chunks to consider
            
        Returns:
            RAGResponse: Answer and source pages
        """
        request_data = RAGQuery(
            question=question,
            document_id=document_id,
            max_chunks=max_chunks
        )
        
        logger.info(f"Sending RAG query for document: {document_id}")
        data = await self._make_request(
            "POST",
            "/rag/ragout",
            json=request_data.model_dump()
        )
        return RAGResponse(**data)

    # Chunk Management Methods
    async def fetch_chunks(
        self, 
        document_id: str | UUID, 
        include_embeddings: bool = False
    ) -> ChunksResponse:
        """
        Fetch chunks for a specific document.
        
        Args:
            document_id (str | UUID): ID of the document
            include_embeddings (bool): Whether to include embeddings in response
            
        Returns:
            ChunksResponse: Document chunks and metadata
        """
        params = {"include_embeddings": "true"} if include_embeddings else None
        
        logger.info(f"Fetching chunks for document: {document_id}")
        data = await self._make_request(
            "GET",
            f"/rag/chunks/{document_id}",
            params=params
        )
        return ChunksResponse(**data)