"""
RAG (Retrieval-Augmented Generation) system for Velero Chatbot
"""
from typing import List, Dict, Any, Optional
from .azure_openai_client import AzureOpenAIClient
from .vector_db import VectorDBInterface
from .document_loader import DocumentLoader


class RAGSystem:
    """RAG system for context-aware question answering"""
    
    def __init__(
        self,
        openai_client: AzureOpenAIClient,
        vector_db: VectorDBInterface,
        top_k: int = 5
    ):
        """
        Initialize RAG system
        
        Args:
            openai_client: Azure OpenAI client
            vector_db: Vector database instance
            top_k: Number of documents to retrieve
        """
        self.openai_client = openai_client
        self.vector_db = vector_db
        self.top_k = top_k
    
    def retrieve_relevant_documents(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query
            top_k: Number of documents to retrieve (overrides default)
            
        Returns:
            List of relevant documents with metadata
        """
        # Generate query embedding
        query_embedding = self.openai_client.generate_embeddings([query])[0]
        
        # Search vector database
        k = top_k or self.top_k
        documents = self.vector_db.search(query_embedding, top_k=k)
        
        return documents
    
    def format_context(self, documents: List[Dict[str, Any]]) -> str:
        """
        Format retrieved documents into context string
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "No relevant context found."
        
        context_parts = []
        for idx, doc in enumerate(documents, 1):
            source = doc.get('source', 'Unknown')
            content = doc.get('content', '')
            score = doc.get('score', 0)
            
            context_parts.append(
                f"[Document {idx} - Source: {source} - Relevance: {score:.2f}]\n{content}\n"
            )
        
        return "\n".join(context_parts)
    
    def answer_query(
        self,
        query: str,
        include_sources: bool = True
    ) -> Dict[str, Any]:
        """
        Answer query using RAG
        
        Args:
            query: User query
            include_sources: Whether to include source documents in response
            
        Returns:
            Dictionary with answer and optional sources
        """
        # Retrieve relevant documents
        documents = self.retrieve_relevant_documents(query)
        
        if not documents:
            # Fallback to direct query if no documents found
            answer = self.openai_client.direct_query(query)
            return {
                'answer': answer,
                'sources': [],
                'method': 'direct'
            }
        
        # Format context
        context = self.format_context(documents)
        
        # Generate answer with context
        answer = self.openai_client.query_with_context(query, context)
        
        result = {
            'answer': answer,
            'method': 'rag'
        }
        
        if include_sources:
            result['sources'] = [
                {
                    'source': doc.get('source', ''),
                    'score': doc.get('score', 0)
                }
                for doc in documents
            ]
        
        return result
    
    def index_repository(
        self,
        document_loader: DocumentLoader,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        batch_size: int = 50
    ) -> bool:
        """
        Index repository documents for RAG
        
        Args:
            document_loader: Document loader instance
            chunk_size: Size of document chunks
            chunk_overlap: Overlap between chunks
            batch_size: Batch size for embedding generation
            
        Returns:
            Success status
        """
        print("Preparing documents for indexing...")
        chunks = document_loader.prepare_documents_for_indexing(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        if not chunks:
            print("No documents to index")
            return False
        
        print(f"Generating embeddings for {len(chunks)} chunks...")
        
        # Generate embeddings in batches
        all_embeddings = []
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [chunk['content'] for chunk in batch]
            
            try:
                embeddings = self.openai_client.generate_embeddings(texts)
                all_embeddings.extend(embeddings)
                print(f"Generated embeddings for {i + len(batch)}/{len(chunks)} chunks")
            except Exception as e:
                print(f"Error generating embeddings for batch {i}: {e}")
                return False
        
        print("Creating/verifying vector database index...")
        # Determine embedding dimension
        dimension = len(all_embeddings[0]) if all_embeddings else 1536
        
        if not self.vector_db.create_index(dimension):
            print("Failed to create index")
            return False
        
        print("Indexing documents in vector database...")
        if not self.vector_db.index_documents(chunks, all_embeddings):
            print("Failed to index documents")
            return False
        
        print("✓ Repository indexing completed successfully!")
        return True
