"""
Configuration module for Velero Chatbot
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class AzureOpenAIConfig:
    """Azure OpenAI configuration"""
    api_key: str
    endpoint: str
    deployment_name: str
    api_version: str
    embedding_deployment: str
    temperature: float = 0.7
    max_tokens: int = 1000


@dataclass
class VectorDBConfig:
    """Vector Database configuration"""
    db_type: str  # pinecone or weaviate
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: Optional[str] = None
    weaviate_url: Optional[str] = None
    weaviate_api_key: Optional[str] = None


@dataclass
class ChatbotConfig:
    """Main chatbot configuration"""
    enable_rag: bool
    chunk_size: int
    chunk_overlap: int
    top_k_results: int
    repo_path: str
    docs_path: str


class Config:
    """Main configuration class"""
    
    def __init__(self):
        self.azure_openai = AzureOpenAIConfig(
            api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", ""),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            embedding_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", ""),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS", "1000"))
        )
        
        self.vector_db = VectorDBConfig(
            db_type=os.getenv("VECTOR_DB_TYPE", "pinecone"),
            pinecone_api_key=os.getenv("PINECONE_API_KEY"),
            pinecone_environment=os.getenv("PINECONE_ENVIRONMENT"),
            pinecone_index_name=os.getenv("PINECONE_INDEX_NAME", "velero-docs"),
            weaviate_url=os.getenv("WEAVIATE_URL", "http://localhost:8080"),
            weaviate_api_key=os.getenv("WEAVIATE_API_KEY")
        )
        
        self.chatbot = ChatbotConfig(
            enable_rag=os.getenv("ENABLE_RAG", "true").lower() == "true",
            chunk_size=int(os.getenv("CHUNK_SIZE", "1000")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "200")),
            top_k_results=int(os.getenv("TOP_K_RESULTS", "5")),
            repo_path=os.getenv("REPO_PATH", "../"),
            docs_path=os.getenv("DOCS_PATH", "../site/content")
        )
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.azure_openai.api_key:
            raise ValueError("AZURE_OPENAI_API_KEY is required")
        if not self.azure_openai.endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT is required")
        if not self.azure_openai.deployment_name:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME is required")
        
        if self.chatbot.enable_rag:
            if self.vector_db.db_type == "pinecone":
                if not self.vector_db.pinecone_api_key:
                    raise ValueError("PINECONE_API_KEY is required when using Pinecone")
            elif self.vector_db.db_type == "weaviate":
                if not self.vector_db.weaviate_url:
                    raise ValueError("WEAVIATE_URL is required when using Weaviate")
        
        return True
