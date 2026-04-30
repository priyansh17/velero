"""
Azure OpenAI integration module for Velero Chatbot
"""
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
from .config import AzureOpenAIConfig


class AzureOpenAIClient:
    """Azure OpenAI client wrapper"""
    
    def __init__(self, config: AzureOpenAIConfig):
        """Initialize Azure OpenAI client"""
        self.config = config
        self.client = AzureOpenAI(
            api_key=config.api_key,
            api_version=config.api_version,
            azure_endpoint=config.endpoint
        )
    
    def generate_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate completion using Azure OpenAI
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (overrides config)
            max_tokens: Maximum tokens to generate (overrides config)
            
        Returns:
            Generated response text
        """
        response = self.client.chat.completions.create(
            model=self.config.deployment_name,
            messages=messages,
            temperature=temperature or self.config.temperature,
            max_tokens=max_tokens or self.config.max_tokens
        )
        return response.choices[0].message.content
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for texts using Azure OpenAI
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        response = self.client.embeddings.create(
            model=self.config.embedding_deployment,
            input=texts
        )
        return [item.embedding for item in response.data]
    
    def query_with_context(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Query with provided context
        
        Args:
            query: User query
            context: Context information
            system_prompt: Optional system prompt
            
        Returns:
            Generated response
        """
        if system_prompt is None:
            system_prompt = (
                "You are a helpful assistant for the Velero project. "
                "Velero is a Kubernetes backup and restore tool. "
                "Answer questions based on the provided context. "
                "If you cannot find the answer in the context, say so clearly."
            )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
        
        return self.generate_completion(messages)
    
    def direct_query(
        self,
        query: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Direct query without context (for non-RAG mode)
        
        Args:
            query: User query
            system_prompt: Optional system prompt
            
        Returns:
            Generated response
        """
        if system_prompt is None:
            system_prompt = (
                "You are a helpful assistant for the Velero project. "
                "Velero is a Kubernetes backup and restore tool that gives you tools to "
                "back up and restore your Kubernetes cluster resources and persistent volumes. "
                "You can run Velero with a public cloud platform or on-premises. "
                "Answer questions about Velero to the best of your knowledge."
            )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        return self.generate_completion(messages)
