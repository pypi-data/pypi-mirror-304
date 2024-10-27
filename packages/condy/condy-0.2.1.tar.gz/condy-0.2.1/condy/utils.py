import re
import logging
from typing import Dict
from .exceptions import ProcessingError

logger = logging.getLogger(__name__)

def process_markdown(content: str) -> Dict[int, str]:
    """Process markdown content into pages"""
    logger.info("Starting markdown processing")
    if not content:
        raise ProcessingError("Empty markdown content")

    try:
        # Split the content into pages
        pages = re.split(r'<!-- PAGE \d+ -->', content)
        pages = [page.strip() for page in pages if page.strip()]

        # Create a dictionary with integer keys
        page_dict = {i: content for i, content in enumerate(pages, start=1)}

        if not page_dict:
            raise ProcessingError("No extractable text found in the markdown")

        logger.info(f"Markdown processing completed. Extracted {len(page_dict)} pages.")
        return page_dict
    except Exception as e:
        logger.error(f"Error processing markdown: {str(e)}")
        raise ProcessingError(f"Failed to process markdown: {str(e)}")