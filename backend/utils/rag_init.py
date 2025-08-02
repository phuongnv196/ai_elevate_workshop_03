"""
Startup initialization for RAG service
Automatically loads law documents when the service starts
"""
import os
import logging
from services.rag_service import rag_service

logger = logging.getLogger(__name__)

def initialize_rag_service():
    """Initialize RAG service with default documents"""
    try:
        # Path to law documents (corrected path)
        pdf_path = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "data", 
            "law_documents.pdf"
        )
        pdf_path = os.path.abspath(pdf_path)
        
        if os.path.exists(pdf_path):
            logger.info("🔄 Loading law documents for RAG service...")
            result = rag_service.load_documents(pdf_path)
            
            if result["success"]:
                logger.info(f"✅ RAG service initialized with {result['chunks_count']} document chunks")
                return True
            else:
                logger.warning(f"⚠️  Failed to load documents: {result.get('error', 'Unknown error')}")
                return False
        else:
            logger.warning(f"⚠️  Law document not found at: {pdf_path}")
            logger.info("RAG service will start without pre-loaded documents")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error initializing RAG service: {e}")
        return False

def check_rag_health():
    """Check RAG service health"""
    try:
        status = rag_service.get_status()
        logger.info(f"RAG Status: {status}")
        return status
    except Exception as e:
        logger.error(f"Error checking RAG health: {e}")
        return None
