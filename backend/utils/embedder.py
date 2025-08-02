"""
Vector embeddings and search utilities for RAG system
Enhanced version from Law_chatbot_project_workshop3
"""
import chromadb
import os
import logging
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for creating and managing text embeddings"""
    
    def __init__(self):
        """Initialize the embedding service"""
        self.client = None
        self.collection = None
        self.collection_name = "law_documents"
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Azure OpenAI client for embeddings"""
        try:
            # Try to get embedding specific API key, fallback to regular API key
            api_key = os.getenv("OPENAI_API_KEY_EMBEDDING") or os.getenv("OPENAI_API_KEY")
            endpoint = os.getenv("OPENAI_ENDPOINT")
            
            if not api_key or not endpoint:
                logger.error("Missing OpenAI API credentials for embeddings")
                return
                
            self.client = AzureOpenAI(
                api_key=api_key,
                api_version="2024-07-01-preview",  # Fixed the typo from original
                azure_endpoint=endpoint
            )
            logger.info("✅ Azure OpenAI embedding client initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize embedding client: {e}")
    
    def embed_text(self, text: str) -> Optional[List[float]]:
        """
        Create embedding for text
        
        Args:
            text (str): Text to embed
            
        Returns:
            Optional[List[float]]: Embedding vector or None if failed
        """
        try:
            if not self.client:
                logger.error("Embedding client not initialized")
                return None
                
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=[text]
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            return None
    
    def build_index(self, chunks: List[str]) -> Optional[chromadb.Collection]:
        """
        Build vector index from text chunks
        
        Args:
            chunks (List[str]): List of text chunks
            
        Returns:
            Optional[chromadb.Collection]: ChromaDB collection or None if failed
        """
        try:
            if not chunks:
                logger.warning("No chunks provided for indexing")
                return None
                
            # Initialize ChromaDB client
            chroma_client = chromadb.Client()
            
            # Delete existing collection if it exists
            try:
                existing_collections = [c.name for c in chroma_client.list_collections()]
                if self.collection_name in existing_collections:
                    chroma_client.delete_collection(self.collection_name)
                    logger.info(f"Deleted existing collection: {self.collection_name}")
            except Exception as e:
                logger.warning(f"Could not delete existing collection: {e}")
            
            # Create new collection
            collection = chroma_client.create_collection(self.collection_name)
            
            # Create embeddings for all chunks
            logger.info(f"Creating embeddings for {len(chunks)} chunks...")
            embeddings = []
            valid_chunks = []
            valid_ids = []
            
            for i, chunk in enumerate(chunks):
                if chunk.strip():  # Only process non-empty chunks
                    embedding = self.embed_text(chunk)
                    if embedding:
                        embeddings.append(embedding)
                        valid_chunks.append(chunk)
                        valid_ids.append(str(i))
            
            if not embeddings:
                logger.error("No valid embeddings created")
                return None
            
            # Add to collection
            collection.add(
                embeddings=embeddings,
                documents=valid_chunks,
                ids=valid_ids
            )
            
            self.collection = collection
            logger.info(f"✅ Built index with {len(embeddings)} embeddings")
            return collection
            
        except Exception as e:
            logger.error(f"Error building index: {e}")
            return None
    
    def search(self, query: str, collection: Optional[chromadb.Collection] = None, k: int = 5) -> List[str]:
        """
        Search for relevant documents
        
        Args:
            query (str): Search query
            collection (Optional[chromadb.Collection]): Collection to search in
            k (int): Number of results to return
            
        Returns:
            List[str]: List of relevant document chunks
        """
        try:
            if not query.strip():
                return []
                
            search_collection = collection or self.collection
            if not search_collection:
                logger.error("No collection available for search")
                return []
            
            # Create query embedding
            query_embedding = self.embed_text(query)
            if not query_embedding:
                logger.error("Could not create query embedding")
                return []
            
            # Perform search
            results = search_collection.query(
                query_embeddings=[query_embedding],
                n_results=min(k, 10)  # Limit max results
            )
            
            # Extract documents from results
            if "documents" in results and results["documents"]:
                documents = results["documents"][0]
                logger.info(f"Found {len(documents)} relevant documents")
                return documents
            
            return []
            
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the current collection
        
        Returns:
            Dict[str, Any]: Collection information
        """
        try:
            if not self.collection:
                return {"status": "No collection loaded", "count": 0}
            
            count = self.collection.count()
            return {
                "status": "Collection loaded",
                "name": self.collection_name,
                "document_count": count
            }
            
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {"status": "Error", "error": str(e)}

# Global instance
embedding_service = EmbeddingService()
