"""
PDF Processing utilities for RAG system
Enhanced version from Law_chatbot_project_workshop3
"""
import fitz  # PyMuPDF
import logging
import os
from typing import List

logger = logging.getLogger(__name__)

def extract_chunks_from_pdf(file_path: str, min_chunk_length: int = 50) -> List[str]:
    """
    Extract text chunks from PDF file
    
    Args:
        file_path (str): Path to PDF file
        min_chunk_length (int): Minimum length of text chunks to include
        
    Returns:
        List[str]: List of text chunks
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"PDF file not found: {file_path}")
            return []
            
        doc = fitz.open(file_path)
        logger.info(f"Processing PDF: {file_path} with {doc.page_count} pages")
        
        chunks = []
        
        for page_num, page in enumerate(doc):
            try:
                text = page.get_text()
                
                # Split into paragraphs and filter by length
                paragraphs = [
                    p.strip() 
                    for p in text.split("\n\n") 
                    if len(p.strip()) > min_chunk_length
                ]
                
                # Add page context to chunks
                for paragraph in paragraphs:
                    chunk_with_context = f"[Page {page_num + 1}] {paragraph}"
                    chunks.append(chunk_with_context)
                    
            except Exception as e:
                logger.warning(f"Error processing page {page_num + 1}: {e}")
                continue
        
        doc.close()
        logger.info(f"Extracted {len(chunks)} chunks from PDF")
        return chunks
        
    except Exception as e:
        logger.error(f"Error processing PDF {file_path}: {e}")
        return []

def extract_text_from_file(file_path: str) -> str:
    """
    Extract all text from PDF file
    
    Args:
        file_path (str): Path to PDF file
        
    Returns:
        str: Full text content
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return ""
            
        doc = fitz.open(file_path)
        full_text = ""
        
        for page in doc:
            full_text += page.get_text() + "\n\n"
        
        doc.close()
        return full_text.strip()
        
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {e}")
        return ""

def validate_pdf_file(file_path: str) -> bool:
    """
    Validate if file is a readable PDF
    
    Args:
        file_path (str): Path to PDF file
        
    Returns:
        bool: True if valid PDF, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            return False
            
        doc = fitz.open(file_path)
        page_count = doc.page_count
        doc.close()
        
        return page_count > 0
        
    except Exception as e:
        logger.error(f"PDF validation failed for {file_path}: {e}")
        return False
