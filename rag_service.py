"""
RAG Service for document processing, embedding, and retrieval
"""

import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
import uuid

# Embedding and vector database
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    logging.warning("sentence-transformers not installed. RAG features will be disabled.")

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    logging.warning("qdrant-client not installed. RAG features will be disabled.")

# Document parsing
try:
    from markitdown import MarkItDown
    MARKITDOWN_AVAILABLE = True
except ImportError:
    MARKITDOWN_AVAILABLE = False
    logging.warning("markitdown not installed. File parsing will be limited.")


class RAGService:
    """Service for handling RAG operations including embedding and retrieval"""
    
    def __init__(self):
        self.enabled = os.environ.get('RAG_ENABLED', 'true').lower() == 'true'
        
        if not self.enabled:
            logging.info("RAG is disabled via configuration")
            return
        
        # Initialize embedding model
        self.embedding_model_name = os.environ.get('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        self.embedding_dimension = int(os.environ.get('EMBEDDING_DIMENSION', 384))
        self.embedding_model = None
        
        if EMBEDDINGS_AVAILABLE:
            try:
                logging.info(f"Loading embedding model: {self.embedding_model_name}")
                self.embedding_model = SentenceTransformer(self.embedding_model_name)
                logging.info("Embedding model loaded successfully")
            except Exception as e:
                logging.error(f"Failed to load embedding model: {e}")
                self.enabled = False
        else:
            self.enabled = False
        
        # Initialize Qdrant client
        self.qdrant_client = None
        self.in_memory = os.environ.get('QDRANT_IN_MEMORY', 'false').lower() == 'true'
        self.qdrant_path = os.environ.get('QDRANT_PATH', './qdrant_storage')

        if QDRANT_AVAILABLE and self.enabled:
            try:
                if self.in_memory:
                    logging.info("Initializing Qdrant in-memory mode (data will not persist)")
                    self.qdrant_client = QdrantClient(":memory:")
                else:
                    # Check if QDRANT_PATH is set (local file storage)
                    if self.qdrant_path and self.qdrant_path != 'localhost':
                        # Use local file-based storage
                        logging.info(f"Initializing Qdrant with persistent storage at: {self.qdrant_path}")
                        os.makedirs(self.qdrant_path, exist_ok=True)
                        self.qdrant_client = QdrantClient(path=self.qdrant_path)
                        logging.info("Qdrant client initialized with persistent file storage")
                    else:
                        # Connect to remote Qdrant server
                        qdrant_host = os.environ.get('QDRANT_HOST', 'localhost')
                        qdrant_port = int(os.environ.get('QDRANT_PORT', 6333))
                        qdrant_api_key = os.environ.get('QDRANT_API_KEY', None)

                        logging.info(f"Connecting to Qdrant server at {qdrant_host}:{qdrant_port}")
                        self.qdrant_client = QdrantClient(
                            host=qdrant_host,
                            port=qdrant_port,
                            api_key=qdrant_api_key if qdrant_api_key else None
                        )
                        logging.info("Qdrant client connected to remote server")
            except Exception as e:
                logging.error(f"Failed to initialize Qdrant client: {e}")
                self.enabled = False
        
        # RAG settings
        self.top_k = int(os.environ.get('RAG_TOP_K', 5))
        self.score_threshold = float(os.environ.get('RAG_SCORE_THRESHOLD', 0.7))
        self.chunk_size = int(os.environ.get('CHUNK_SIZE', 500))
        self.chunk_overlap = int(os.environ.get('CHUNK_OVERLAP', 50))
        
        # Initialize MarkItDown
        self.markitdown = None
        if MARKITDOWN_AVAILABLE:
            try:
                self.markitdown = MarkItDown()
                logging.info("MarkItDown initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize MarkItDown: {e}")
    
    def is_available(self) -> bool:
        """Check if RAG service is available and enabled"""
        return self.enabled and self.embedding_model is not None and self.qdrant_client is not None
    
    def create_knowledge_base(self, kb_name: str) -> bool:
        """Create a new knowledge base (collection) in Qdrant"""
        if not self.is_available():
            return False
        
        try:
            # Check if collection already exists
            collections = self.qdrant_client.get_collections().collections
            if any(col.name == kb_name for col in collections):
                logging.info(f"Knowledge base '{kb_name}' already exists")
                return True
            
            # Create new collection
            self.qdrant_client.create_collection(
                collection_name=kb_name,
                vectors_config=VectorParams(
                    size=self.embedding_dimension,
                    distance=Distance.COSINE
                )
            )
            logging.info(f"Created knowledge base: {kb_name}")
            return True
        except Exception as e:
            logging.error(f"Failed to create knowledge base '{kb_name}': {e}")
            return False
    
    def list_knowledge_bases(self) -> List[Dict[str, Any]]:
        """List all knowledge bases"""
        if not self.is_available():
            return []
        
        try:
            collections = self.qdrant_client.get_collections().collections
            return [
                {
                    'name': col.name,
                    'vectors_count': self.qdrant_client.count(col.name).count
                }
                for col in collections
            ]
        except Exception as e:
            logging.error(f"Failed to list knowledge bases: {e}")
            return []
    
    def delete_knowledge_base(self, kb_name: str) -> bool:
        """Delete a knowledge base"""
        if not self.is_available():
            return False
        
        try:
            self.qdrant_client.delete_collection(kb_name)
            logging.info(f"Deleted knowledge base: {kb_name}")
            return True
        except Exception as e:
            logging.error(f"Failed to delete knowledge base '{kb_name}': {e}")
            return False
    
    def parse_file(self, file_path: str) -> Optional[str]:
        """Parse a file and extract text content using MarkItDown"""
        if not self.markitdown:
            logging.warning("MarkItDown not available, attempting basic text extraction")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                logging.error(f"Failed to read file: {e}")
                return None
        
        try:
            result = self.markitdown.convert(file_path)
            return result.text_content
        except Exception as e:
            logging.error(f"Failed to parse file with MarkItDown: {e}")
            return None
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > self.chunk_size // 2:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - self.chunk_overlap
        
        return [c for c in chunks if c]  # Filter empty chunks
    
    def embed_text(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text"""
        if not self.embedding_model:
            return None
        
        try:
            embedding = self.embedding_model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logging.error(f"Failed to generate embedding: {e}")
            return None
    
    def add_document(self, kb_name: str, file_path: str, metadata: Optional[Dict] = None) -> bool:
        """Add a document to a knowledge base"""
        if not self.is_available():
            return False
        
        # Ensure knowledge base exists
        self.create_knowledge_base(kb_name)
        
        # Parse file
        text = self.parse_file(file_path)
        if not text:
            logging.error(f"Failed to parse file: {file_path}")
            return False
        
        # Chunk text
        chunks = self.chunk_text(text)
        logging.info(f"Split document into {len(chunks)} chunks")
        
        # Generate document ID
        file_name = Path(file_path).name
        doc_id = hashlib.md5(file_name.encode()).hexdigest()
        
        # Prepare points for Qdrant
        points = []
        for i, chunk in enumerate(chunks):
            embedding = self.embed_text(chunk)
            if not embedding:
                continue

            point_metadata = {
                'document_id': doc_id,
                'file_name': file_name,
                'chunk_index': i,
                'text': chunk,
                **(metadata or {})
            }

            # Generate a valid UUID from the document ID and chunk index
            # Use UUID5 with a namespace to ensure deterministic IDs
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{doc_id}_{i}"))

            points.append(PointStruct(
                id=point_id,
                vector=embedding,
                payload=point_metadata
            ))
        
        # Upload to Qdrant
        try:
            self.qdrant_client.upsert(
                collection_name=kb_name,
                points=points
            )
            logging.info(f"Added {len(points)} chunks from '{file_name}' to '{kb_name}'")
            return True
        except Exception as e:
            logging.error(f"Failed to add document to Qdrant: {e}")
            return False
    
    def search(self, kb_name: str, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search for relevant documents in a knowledge base"""
        if not self.is_available():
            logging.warning("RAG service not available for search")
            return []

        top_k = top_k or self.top_k

        # Generate query embedding
        query_embedding = self.embed_text(query)
        if not query_embedding:
            logging.error("Failed to generate query embedding")
            return []

        try:
            # Search with a lower threshold to get more results
            # We'll use 0.3 instead of the configured threshold for better recall
            results = self.qdrant_client.search(
                collection_name=kb_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=0.3  # Lower threshold for better recall
            )

            logging.info(f"Qdrant search returned {len(results)} results (threshold: 0.3)")

            # Log the scores to help debug
            if results:
                scores = [hit.score for hit in results]
                logging.info(f"Result scores: min={min(scores):.3f}, max={max(scores):.3f}, avg={sum(scores)/len(scores):.3f}")

            formatted_results = [
                {
                    'text': hit.payload.get('text', ''),
                    'score': hit.score,
                    'file_name': hit.payload.get('file_name', ''),
                    'metadata': hit.payload
                }
                for hit in results
            ]

            # Log what we're returning
            if formatted_results:
                logging.info(f"Returning {len(formatted_results)} results:")
                for i, result in enumerate(formatted_results[:3], 1):  # Log first 3
                    logging.info(f"  {i}. {result['file_name']} (score: {result['score']:.3f}) - {result['text'][:100]}...")

            return formatted_results

        except Exception as e:
            logging.error(f"Failed to search in knowledge base '{kb_name}': {e}")
            import traceback
            logging.error(traceback.format_exc())
            return []


# Global RAG service instance
rag_service = RAGService()
