import httpx
import logging
from typing import Dict, Optional, Union
from .exceptions import NetworkError, TimeoutError, APIError
from .utils import process_markdown, process_text
from .models import DocumentOutput, Pages, RAGQuery, RAGResponse, ChunksResponse

logger = logging.getLogger(__name__)

class CondyClient:
    """Client for interacting with the Condensation.ai API"""
    
    def __init__(
        self, 
        api_key: str,
        base_url: str = "https://api.condensation.ai",
        timeout: float = 30.0,
        verbose: bool = False
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verbose = verbose
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }

    def _log(self, level: str, message: str) -> None:
        """Internal logging method that respects verbose setting"""
        if self.verbose:
            getattr(logger, level)(message)

    async def fetch_content(self, url: str) -> str:
        """Fetch content from a URL"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.text
            except httpx.TimeoutException as e:
                self._log("error", f"Content fetch timed out: {str(e)}")
                raise TimeoutError("Timeout while fetching content") from e
            except httpx.RequestError as e:
                self._log("error", f"Network error during content fetch: {str(e)}")
                raise NetworkError("Network error while fetching content") from e

    async def upload_pages(self, pages: Dict[int, str]) -> DocumentOutput:
        """Upload pages to the API"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/rag/raginmultipage",
                    json={"pages": pages},
                    headers=self.headers
                )
                
                if not response.is_success:
                    self._log("error", f"Error response: {response.status_code}")
                    self._log("error", f"Response body: {response.json()}")
                    raise APIError(
                        response.status_code,
                        response.json().get('detail', 'Unknown error')
                    )
                    
                return response.json()
                
            except httpx.TimeoutException as e:
                self._log("error", f"Upload request timed out: {str(e)}")
                raise TimeoutError("Request timed out") from e
            except httpx.RequestError as e:
                self._log("error", f"Network error during upload: {str(e)}")
                raise NetworkError("Network error occurred") from e

    async def query_rag(
        self, 
        question: str, 
        document_id: str, 
        max_chunks: int = 5
    ) -> RAGResponse:
        """Query the RAG system"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                request_data = RAGQuery(
                    question=question,
                    document_id=document_id,
                    max_chunks=max_chunks
                )
                
                response = await client.post(
                    f"{self.base_url}/rag/ragout",
                    json=request_data.model_dump(),
                    headers=self.headers
                )
                
                if not response.is_success:
                    self._log("error", f"Error response: {response.status_code}")
                    self._log("error", f"Response body: {response.json()}")
                    raise APIError(
                        response.status_code,
                        response.json().get('detail', 'Unknown error')
                    )
                
                return RAGResponse(**response.json())
                
            except httpx.TimeoutException as e:
                self._log("error", f"Request timed out: {str(e)}")
                raise TimeoutError("Request timed out") from e
            except httpx.RequestError as e:
                self._log("error", f"Network error occurred: {str(e)}")
                raise NetworkError("Network error occurred") from e

    async def fetch_chunks(
        self, 
        document_id: str, 
        include_embeddings: bool = False
    ) -> ChunksResponse:
        """Fetch chunks for a document"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                url = f"{self.base_url}/rag/chunks/{document_id}"
                if include_embeddings:
                    url += "?include_embeddings=true"
                
                response = await client.get(
                    url,
                    headers=self.headers
                )
                
                if not response.is_success:
                    self._log("error", f"Error response: {response.status_code}")
                    self._log("error", f"Response body: {response.json()}")
                    raise APIError(
                        response.status_code,
                        response.json().get('detail', 'Unknown error')
                    )
                
                return ChunksResponse(**response.json())
                
            except httpx.TimeoutException as e:
                self._log("error", f"Request timed out: {str(e)}")
                raise TimeoutError("Request timed out") from e
            except httpx.RequestError as e:
                self._log("error", f"Network error occurred: {str(e)}")
                raise NetworkError("Network error occurred") from e

    async def process_document(
        self,
        url: Optional[str] = None,
        content: Optional[str] = None,
        content_type: str = "markdown"
    ) -> DocumentOutput:
        """Process and upload a document"""
        try:
            # Get content either from URL or direct input
            if url:
                self._log("info", "Fetching content from URL...")
                document_content = await self.fetch_content(url)
            elif content:
                document_content = content
            else:
                raise ValueError("Either url or content must be provided")

            # Process content based on type
            self._log("info", f"Processing content as {content_type}...")
            if content_type == "markdown":
                pages_dict = process_markdown(document_content)
            else:
                pages_dict = process_text(document_content)

            # Upload to API
            self._log("info", f"Uploading {len(pages_dict)} pages...")
            return await self.upload_pages(pages_dict)

        except Exception as e:
            self._log("error", f"Error processing document: {str(e)}")
            raise