"""
Document indexing pipeline for Velero documentation
"""
import os
from pathlib import Path
from typing import List, Dict, Any
import re
from tqdm import tqdm


class DocumentLoader:
    """Load and process documents from the repository"""
    
    def __init__(self, repo_path: str, docs_path: str):
        """
        Initialize document loader
        
        Args:
            repo_path: Path to repository root
            docs_path: Path to documentation directory
        """
        self.repo_path = Path(repo_path)
        self.docs_path = Path(docs_path)
    
    def load_markdown_files(self) -> List[Dict[str, Any]]:
        """
        Load all markdown files from documentation
        
        Returns:
            List of document dictionaries with content and metadata
        """
        documents = []
        
        # Load from docs directory
        if self.docs_path.exists():
            md_files = list(self.docs_path.rglob("*.md"))
            for file_path in tqdm(md_files, desc="Loading documentation files"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append({
                            'content': content,
                            'source': str(file_path.relative_to(self.repo_path)),
                            'type': 'documentation'
                        })
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        
        # Load key repository files
        key_files = [
            'README.md',
            'CONTRIBUTING.md',
            'GOVERNANCE.md',
            'SECURITY.md',
            'CHANGELOG.md'
        ]
        
        for filename in key_files:
            file_path = self.repo_path / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append({
                            'content': content,
                            'source': filename,
                            'type': 'repository'
                        })
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        return documents
    
    def chunk_documents(
        self,
        documents: List[Dict[str, Any]],
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[Dict[str, Any]]:
        """
        Split documents into chunks
        
        Args:
            documents: List of documents to chunk
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of chunked documents with metadata
        """
        chunks = []
        
        for doc in tqdm(documents, desc="Chunking documents"):
            content = doc['content']
            source = doc['source']
            doc_type = doc['type']
            
            # Split by paragraphs first
            paragraphs = re.split(r'\n\s*\n', content)
            
            current_chunk = ""
            chunk_idx = 0
            
            for para in paragraphs:
                # If adding this paragraph exceeds chunk size, save current chunk
                if len(current_chunk) + len(para) > chunk_size and current_chunk:
                    chunks.append({
                        'content': current_chunk.strip(),
                        'source': source,
                        'type': doc_type,
                        'chunk_id': chunk_idx
                    })
                    
                    # Start new chunk with overlap
                    overlap_text = current_chunk[-chunk_overlap:] if len(current_chunk) > chunk_overlap else current_chunk
                    current_chunk = overlap_text + "\n\n" + para
                    chunk_idx += 1
                else:
                    current_chunk += "\n\n" + para if current_chunk else para
            
            # Add remaining content
            if current_chunk.strip():
                chunks.append({
                    'content': current_chunk.strip(),
                    'source': source,
                    'type': doc_type,
                    'chunk_id': chunk_idx
                })
        
        return chunks
    
    def prepare_documents_for_indexing(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[Dict[str, Any]]:
        """
        Complete pipeline to prepare documents for indexing
        
        Args:
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of prepared document chunks
        """
        print("Loading documents...")
        documents = self.load_markdown_files()
        print(f"Loaded {len(documents)} documents")
        
        print("Chunking documents...")
        chunks = self.chunk_documents(documents, chunk_size, chunk_overlap)
        print(f"Created {len(chunks)} chunks")
        
        return chunks
