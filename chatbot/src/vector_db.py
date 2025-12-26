"""
Vector database integration module
"""
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import time


class VectorDBInterface(ABC):
    """Abstract interface for vector database operations"""
    
    @abstractmethod
    def create_index(self, dimension: int) -> bool:
        """Create vector index"""
        pass
    
    @abstractmethod
    def index_documents(
        self,
        documents: List[Dict[str, Any]],
        embeddings: List[List[float]]
    ) -> bool:
        """Index documents with their embeddings"""
        pass
    
    @abstractmethod
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        pass
    
    @abstractmethod
    def index_exists(self) -> bool:
        """Check if index exists"""
        pass


class PineconeDB(VectorDBInterface):
    """Pinecone vector database implementation"""
    
    def __init__(self, api_key: str, environment: str, index_name: str):
        """Initialize Pinecone client"""
        try:
            from pinecone import Pinecone, ServerlessSpec
            
            self.pc = Pinecone(api_key=api_key)
            self.index_name = index_name
            self.environment = environment
            self.index = None
            
            # Connect to index if it exists
            if self.index_exists():
                self.index = self.pc.Index(index_name)
        except ImportError:
            raise ImportError("Please install pinecone-client: pip install pinecone-client")
    
    def index_exists(self) -> bool:
        """Check if index exists"""
        try:
            indexes = self.pc.list_indexes()
            return any(idx.name == self.index_name for idx in indexes)
        except Exception as e:
            print(f"Error checking index existence: {e}")
            return False
    
    def create_index(self, dimension: int = 1536) -> bool:
        """Create Pinecone index"""
        try:
            if self.index_exists():
                print(f"Index {self.index_name} already exists")
                self.index = self.pc.Index(self.index_name)
                return True
            
            from pinecone import ServerlessSpec
            
            self.pc.create_index(
                name=self.index_name,
                dimension=dimension,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            
            # Wait for index to be ready
            time.sleep(5)
            self.index = self.pc.Index(self.index_name)
            print(f"Created index {self.index_name}")
            return True
        except Exception as e:
            print(f"Error creating index: {e}")
            return False
    
    def index_documents(
        self,
        documents: List[Dict[str, Any]],
        embeddings: List[List[float]]
    ) -> bool:
        """Index documents in Pinecone"""
        if not self.index:
            print("Index not initialized")
            return False
        
        try:
            vectors = []
            for idx, (doc, embedding) in enumerate(zip(documents, embeddings)):
                vectors.append({
                    'id': f"doc_{idx}",
                    'values': embedding,
                    'metadata': {
                        'content': doc['content'][:1000],  # Limit metadata size
                        'source': doc['source'],
                        'type': doc['type'],
                        'chunk_id': doc.get('chunk_id', 0)
                    }
                })
            
            # Batch upsert
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
            print(f"Indexed {len(documents)} documents")
            return True
        except Exception as e:
            print(f"Error indexing documents: {e}")
            return False
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        if not self.index:
            print("Index not initialized")
            return []
        
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            documents = []
            for match in results.matches:
                documents.append({
                    'content': match.metadata.get('content', ''),
                    'source': match.metadata.get('source', ''),
                    'score': match.score
                })
            
            return documents
        except Exception as e:
            print(f"Error searching: {e}")
            return []


class WeaviateDB(VectorDBInterface):
    """Weaviate vector database implementation"""
    
    def __init__(self, url: str, api_key: Optional[str] = None):
        """Initialize Weaviate client"""
        try:
            import weaviate
            from weaviate.auth import AuthApiKey
            
            if api_key:
                auth_config = AuthApiKey(api_key=api_key)
                self.client = weaviate.Client(url=url, auth_client_secret=auth_config)
            else:
                self.client = weaviate.Client(url=url)
            
            self.class_name = "VeleroDocument"
        except ImportError:
            raise ImportError("Please install weaviate-client: pip install weaviate-client")
    
    def index_exists(self) -> bool:
        """Check if class exists"""
        try:
            schema = self.client.schema.get()
            return any(cls['class'] == self.class_name for cls in schema.get('classes', []))
        except Exception as e:
            print(f"Error checking schema: {e}")
            return False
    
    def create_index(self, dimension: int = 1536) -> bool:
        """Create Weaviate class schema"""
        try:
            if self.index_exists():
                print(f"Class {self.class_name} already exists")
                return True
            
            class_obj = {
                "class": self.class_name,
                "description": "Velero documentation and repository content",
                "vectorizer": "none",  # We'll provide vectors
                "properties": [
                    {
                        "name": "content",
                        "dataType": ["text"],
                        "description": "Document content"
                    },
                    {
                        "name": "source",
                        "dataType": ["string"],
                        "description": "Source file path"
                    },
                    {
                        "name": "type",
                        "dataType": ["string"],
                        "description": "Document type"
                    },
                    {
                        "name": "chunk_id",
                        "dataType": ["int"],
                        "description": "Chunk identifier"
                    }
                ]
            }
            
            self.client.schema.create_class(class_obj)
            print(f"Created class {self.class_name}")
            return True
        except Exception as e:
            print(f"Error creating class: {e}")
            return False
    
    def index_documents(
        self,
        documents: List[Dict[str, Any]],
        embeddings: List[List[float]]
    ) -> bool:
        """Index documents in Weaviate"""
        try:
            with self.client.batch as batch:
                batch.batch_size = 100
                
                for doc, embedding in zip(documents, embeddings):
                    properties = {
                        "content": doc['content'],
                        "source": doc['source'],
                        "type": doc['type'],
                        "chunk_id": doc.get('chunk_id', 0)
                    }
                    
                    batch.add_data_object(
                        data_object=properties,
                        class_name=self.class_name,
                        vector=embedding
                    )
            
            print(f"Indexed {len(documents)} documents")
            return True
        except Exception as e:
            print(f"Error indexing documents: {e}")
            return False
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            result = (
                self.client.query
                .get(self.class_name, ["content", "source"])
                .with_near_vector({"vector": query_embedding})
                .with_limit(top_k)
                .with_additional(["distance"])
                .do()
            )
            
            documents = []
            if result and "data" in result:
                items = result["data"]["Get"][self.class_name]
                for item in items:
                    documents.append({
                        'content': item.get('content', ''),
                        'source': item.get('source', ''),
                        'score': 1 - item['_additional']['distance']  # Convert distance to similarity
                    })
            
            return documents
        except Exception as e:
            print(f"Error searching: {e}")
            return []


def get_vector_db(db_type: str, **kwargs) -> VectorDBInterface:
    """
    Factory function to get vector database instance
    
    Args:
        db_type: Type of vector database ('pinecone' or 'weaviate')
        **kwargs: Database-specific configuration
        
    Returns:
        Vector database instance
    """
    if db_type == "pinecone":
        return PineconeDB(
            api_key=kwargs['api_key'],
            environment=kwargs['environment'],
            index_name=kwargs['index_name']
        )
    elif db_type == "weaviate":
        return WeaviateDB(
            url=kwargs['url'],
            api_key=kwargs.get('api_key')
        )
    else:
        raise ValueError(f"Unsupported vector database type: {db_type}")
