"""
Main chatbot module for Velero
"""
from typing import Optional, Dict, Any
from .config import Config
from .azure_openai_client import AzureOpenAIClient
from .vector_db import get_vector_db, VectorDBInterface
from .document_loader import DocumentLoader
from .rag_system import RAGSystem


class VeleroChatbot:
    """Main chatbot class"""
    
    def __init__(self, config: Config):
        """
        Initialize Velero Chatbot
        
        Args:
            config: Configuration object
        """
        self.config = config
        config.validate()
        
        # Initialize Azure OpenAI client
        self.openai_client = AzureOpenAIClient(config.azure_openai)
        
        # Initialize vector database if RAG is enabled
        self.vector_db: Optional[VectorDBInterface] = None
        self.rag_system: Optional[RAGSystem] = None
        
        if config.chatbot.enable_rag:
            self._initialize_rag()
    
    def _initialize_rag(self):
        """Initialize RAG components"""
        try:
            if self.config.vector_db.db_type == "pinecone":
                self.vector_db = get_vector_db(
                    "pinecone",
                    api_key=self.config.vector_db.pinecone_api_key,
                    environment=self.config.vector_db.pinecone_environment,
                    index_name=self.config.vector_db.pinecone_index_name
                )
            elif self.config.vector_db.db_type == "weaviate":
                self.vector_db = get_vector_db(
                    "weaviate",
                    url=self.config.vector_db.weaviate_url,
                    api_key=self.config.vector_db.weaviate_api_key
                )
            else:
                raise ValueError(f"Unsupported vector DB type: {self.config.vector_db.db_type}")
            
            self.rag_system = RAGSystem(
                openai_client=self.openai_client,
                vector_db=self.vector_db,
                top_k=self.config.chatbot.top_k_results
            )
            
            print(f"✓ RAG system initialized with {self.config.vector_db.db_type}")
        except Exception as e:
            print(f"Warning: Failed to initialize RAG system: {e}")
            print("Falling back to direct query mode")
            self.config.chatbot.enable_rag = False
    
    def index_repository(self) -> bool:
        """
        Index repository documents for RAG
        
        Returns:
            Success status
        """
        if not self.config.chatbot.enable_rag or not self.rag_system:
            print("RAG is not enabled or initialized")
            return False
        
        document_loader = DocumentLoader(
            repo_path=self.config.chatbot.repo_path,
            docs_path=self.config.chatbot.docs_path
        )
        
        return self.rag_system.index_repository(
            document_loader=document_loader,
            chunk_size=self.config.chatbot.chunk_size,
            chunk_overlap=self.config.chatbot.chunk_overlap
        )
    
    def query(self, question: str, include_sources: bool = True) -> Dict[str, Any]:
        """
        Process a user query
        
        Args:
            question: User question
            include_sources: Whether to include sources in response
            
        Returns:
            Response dictionary with answer and metadata
        """
        if not question or not question.strip():
            return {
                'answer': "Please provide a valid question.",
                'sources': [],
                'method': 'validation'
            }
        
        # Check if question is about Velero
        if not self._is_velero_related(question):
            return {
                'answer': (
                    "I'm specialized in answering questions about the Velero project "
                    "(Kubernetes backup and restore tool). Please ask questions related to Velero."
                ),
                'sources': [],
                'method': 'validation'
            }
        
        # Use RAG if enabled and initialized
        if self.config.chatbot.enable_rag and self.rag_system:
            try:
                return self.rag_system.answer_query(question, include_sources)
            except Exception as e:
                print(f"Error in RAG query: {e}")
                print("Falling back to direct query")
        
        # Fallback to direct query
        try:
            answer = self.openai_client.direct_query(question)
            return {
                'answer': answer,
                'sources': [],
                'method': 'direct'
            }
        except Exception as e:
            return {
                'answer': f"Error processing query: {str(e)}",
                'sources': [],
                'method': 'error'
            }
    
    def _is_velero_related(self, question: str) -> bool:
        """
        Check if question is related to Velero (basic heuristic)
        
        Args:
            question: User question
            
        Returns:
            True if likely Velero-related, False otherwise
        """
        # Keywords that indicate Velero-related questions
        velero_keywords = [
            'velero', 'backup', 'restore', 'kubernetes', 'k8s',
            'cluster', 'migration', 'snapshot', 'persistent volume',
            'pv', 'pvc', 'restic', 'csi', 'schedule'
        ]
        
        question_lower = question.lower()
        
        # If question contains Velero keywords, it's related
        if any(keyword in question_lower for keyword in velero_keywords):
            return True
        
        # For generic questions about documentation or help, allow them
        generic_keywords = ['how', 'what', 'why', 'when', 'where', 'explain', 'tell']
        if any(keyword in question_lower for keyword in generic_keywords):
            return True
        
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get chatbot status
        
        Returns:
            Status dictionary
        """
        status = {
            'rag_enabled': self.config.chatbot.enable_rag,
            'vector_db_type': self.config.vector_db.db_type if self.config.chatbot.enable_rag else None,
            'vector_db_ready': False
        }
        
        if self.config.chatbot.enable_rag and self.vector_db:
            try:
                status['vector_db_ready'] = self.vector_db.index_exists()
            except:
                status['vector_db_ready'] = False
        
        return status
