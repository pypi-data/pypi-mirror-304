import re
import requests
import json
from typing import Optional, Dict, Any, List

class ReadPDFs:
    def __init__(self, api_key: str, base_url: str = "https://backend.readpdfs.com"):
        self.api_key = api_key
        self.base_url = base_url
    def process_pdf(self, 
                    pdf_url: Optional[str] = None, 
                    file_path: Optional[str] = None,
                    file_content: Optional[bytes] = None,
                    filename: Optional[str] = None,
                    quality: str = "standard") -> Dict[str, Any]:
        """
        Process a PDF file and convert it to markdown.
        """
        endpoint = f"{self.base_url}/process_pdf/"
        headers = {
            "x-api-key": self.api_key,
        }
        
        # Validate inputs
        provided_inputs = sum(1 for x in [pdf_url, file_path, file_content] if x is not None)
        if provided_inputs != 1:
            raise ValueError("Provide exactly one of: pdf_url, file_path, or file_content")
        
        if file_content and not filename:
            raise ValueError("filename must be provided when using file_content")
            
        # Handle different input types
        if pdf_url:
            data = {
                "pdf_url": pdf_url,
                "quality": quality
            }
            response = requests.post(endpoint, headers=headers, json=data)
        else:
            # File upload processing (either from path or content)
            files = None
            if file_path:
                files = {
                    "pdf": ("document.pdf", open(file_path, "rb"), "application/pdf")
                }
            else:
                files = {
                    "pdf": (filename, file_content, "application/pdf")
                }
                
            response = requests.post(
                endpoint, 
                headers=headers,
                files=files,
                data={"quality": quality}
            )
            
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        
    def fetch_markdown(self, url: str) -> str:
        """
        Fetch the markdown content from a given URL.
        Args:
            url (str): URL of the markdown content.
        Returns:
            str: The markdown content.
        """
        endpoint = f"{self.base_url}/fetch_markdown/"
        params = {"url": url}
        response = requests.get(endpoint, params=params)
        
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def process_markdown(self, content: str) -> Dict[int, str]:
        """
        Process markdown content and split it into pages.
        Args:
            content (str): The markdown content to process.
        Returns:
            Dict[int, str]: Dictionary of page numbers and their content.
        """
        if not content:
            raise ValueError("Empty markdown content")

        try:
            pages = re.split(r'<!-- PAGE \d+ -->', content)
            pages = [page.strip() for page in pages if page.strip()]
            page_dict = {i: content for i, content in enumerate(pages, start=1)}

            if not page_dict:
                raise ValueError("No extractable text found in the markdown")

            return page_dict
        except Exception as e:
            raise ValueError(f"Failed to process markdown: {str(e)}")

