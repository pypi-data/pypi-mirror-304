import httpx
import logging
from typing import Optional
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
from .utils import process_markdown

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
        """
        Internal method to make HTTP requests.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            json (Optional[dict]): JSON body for POST requests
            params (Optional[dict]): Query parameters
            
        Returns:
            dict: Response data
        """
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
    async def fetch_markdown(self, url: str) -> str:
        """
        Fetch markdown content from a URL.
        
        Args:
            url (str): URL of the markdown document
            
        Returns:
            str: Markdown content
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.text
            except httpx.TimeoutException as e:
                logger.error(f"Markdown fetch timed out: {str(e)}")
                raise TimeoutError("Timeout while fetching markdown") from e
            except httpx.RequestError as e:
                logger.error(f"Network error during markdown fetch: {str(e)}")
                raise NetworkError("Network error while fetching markdown") from e

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

    async def process_document(self, markdown_url: str) -> DocumentOutput:
        """
        Convenience method to process a document from URL to upload.
        
        Args:
            markdown_url (str): URL of the markdown document
            
        Returns:
            DocumentOutput: Upload result containing document ID
        """
        markdown_content = await self.fetch_markdown(markdown_url)
        pages_dict = process_markdown(markdown_content)
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