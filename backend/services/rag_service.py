"""
RAG (Retrieval-Augmented Generation) Service
Integrates PDF processing, embeddings, and AI chat for legal document Q&A
"""
import os
import logging
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
from utils.pdf_processor import extract_chunks_from_pdf, validate_pdf_file
from utils.embedder import embedding_service
from utils.prompts import build_law_prompt, build_system_prompt, build_search_prompt

logger = logging.getLogger(__name__)

class RAGService:
    """Service for RAG-based legal document Q&A"""
    
    def __init__(self):
        """Initialize the RAG service"""
        self.client = None
        self.documents_loaded = False
        self.document_chunks = []
        self.collection = None
        self._initialize_openai_client()
    
    def _initialize_openai_client(self):
        """Initialize Azure OpenAI client for chat completion"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            endpoint = os.getenv("OPENAI_ENDPOINT")
            
            if not api_key or not endpoint:
                logger.error("Missing OpenAI API credentials for chat completion")
                return
                
            self.client = AzureOpenAI(
                api_key=api_key,
                api_version="2024-07-01-preview",
                azure_endpoint=endpoint
            )
            logger.info("✅ Azure OpenAI chat client initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
    
    def load_documents(self, pdf_path: str) -> Dict[str, Any]:
        """
        Load and process PDF documents for RAG
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            Dict[str, Any]: Loading status and information
        """
        try:
            logger.info(f"Loading documents from: {pdf_path}")
            
            # Validate PDF file
            if not validate_pdf_file(pdf_path):
                return {
                    "success": False,
                    "error": f"Invalid or unreadable PDF file: {pdf_path}"
                }
            
            # Extract chunks from PDF
            chunks = extract_chunks_from_pdf(pdf_path)
            if not chunks:
                return {
                    "success": False,
                    "error": "No text chunks extracted from PDF"
                }
            
            self.document_chunks = chunks
            
            # Build vector index
            collection = embedding_service.build_index(chunks)
            if not collection:
                return {
                    "success": False,
                    "error": "Failed to build vector index"
                }
            
            self.collection = collection
            self.documents_loaded = True
            
            logger.info(f"✅ Successfully loaded {len(chunks)} document chunks")
            
            return {
                "success": True,
                "chunks_count": len(chunks),
                "message": f"Successfully loaded {len(chunks)} document chunks"
            }
            
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            return {
                "success": False,
                "error": f"Failed to load documents: {str(e)}"
            }
    
    def search_documents(self, query: str, k: int = 5) -> List[str]:
        """
        Search for relevant document chunks
        
        Args:
            query (str): Search query
            k (int): Number of results to return
            
        Returns:
            List[str]: Relevant document chunks
        """
        try:
            if not self.documents_loaded:
                logger.warning("No documents loaded for search")
                return []
            
            # Enhance search query
            enhanced_query = build_search_prompt(query)
            
            # Perform search
            results = embedding_service.search(enhanced_query, self.collection, k)
            
            logger.info(f"Search for '{query}' returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    def chat_with_context(self, user_message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Generate AI response with RAG context
        
        Args:
            user_message (str): User's message/question
            conversation_history (List[Dict], optional): Previous conversation messages
            
        Returns:
            Dict[str, Any]: AI response with metadata
        """
        try:
            if not self.client:
                return {
                    "success": False,
                    "error": "OpenAI client not initialized"
                }
            
            # Search for relevant context
            context_snippets = []
            if self.documents_loaded:
                context_snippets = self.search_documents(user_message, k=5)
            
            # Build prompt with context
            if context_snippets:
                full_prompt = build_law_prompt(user_message, context_snippets)
                response_type = "rag"
            else:
                full_prompt = user_message
                response_type = "general"
            
            # Prepare messages for chat completion
            messages = [{"role": "system", "content": build_system_prompt()}]
            
            # Add conversation history (last 4 messages to stay within token limits)
            if conversation_history:
                messages.extend(conversation_history[-4:])
            
            # Add current prompt
            messages.append({"role": "user", "content": full_prompt})
            
            # Generate response
            completion = self.client.chat.completions.create(
                model="GPT-4.1",  # Updated model name
                messages=messages,
                temperature=0.1,  # Lower temperature for more consistent legal advice
                max_tokens=1000
            )
            
            response_content = completion.choices[0].message.content
            
            return {
                "success": True,
                "response": response_content,
                "context_used": len(context_snippets),
                "context_snippets": context_snippets[:3],  # First 3 for reference
                "response_type": response_type,
                "tokens_used": completion.usage.total_tokens if completion.usage else None
            }
            
        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            return {
                "success": False,
                "error": f"Failed to generate response: {str(e)}"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get RAG service status
        
        Returns:
            Dict[str, Any]: Service status information
        """
        try:
            collection_info = embedding_service.get_collection_info()
            
            return {
                "openai_client": self.client is not None,
                "documents_loaded": self.documents_loaded,
                "chunks_count": len(self.document_chunks),
                "collection_info": collection_info,
                "embedding_service": embedding_service.client is not None
            }
            
        except Exception as e:
            logger.error(f"Error getting RAG status: {e}")
            return {
                "error": str(e)
            }
    
    def reload_documents(self, pdf_path: str = None) -> Dict[str, Any]:
        """
        Reload documents from PDF
        
        Args:
            pdf_path (str, optional): Path to PDF file, uses default if None
            
        Returns:
            Dict[str, Any]: Reload status
        """
        try:
            # Use default PDF path if not provided
            if pdf_path is None:
                pdf_path = os.path.join(os.path.dirname(__file__), "..", "data", "law_documents.pdf")
            
            # Reset state
            self.documents_loaded = False
            self.document_chunks = []
            self.collection = None
            
            # Reload documents
            return self.load_documents(pdf_path)
            
        except Exception as e:
            logger.error(f"Error reloading documents: {e}")
            return {
                "success": False,
                "error": f"Failed to reload documents: {str(e)}"
            }

# Global RAG service instance
rag_service = RAGService()
