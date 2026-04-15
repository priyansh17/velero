# Velero Chatbot Architecture

## Overview

The Velero Chatbot is designed as a modular, extensible system that can operate in two modes:
1. **Direct Mode**: Uses Azure OpenAI directly for query answering
2. **RAG Mode**: Retrieval-Augmented Generation with vector database for context-aware responses

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                      (CLI / Web - Future)                        │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Chatbot Controller                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ - Query validation (Velero-related)                      │  │
│  │ - Mode routing (RAG vs Direct)                           │  │
│  │ - Error handling                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────┬──────────────────────────┬──────────────────┘
                    │                          │
         ┌──────────▼─────────┐     ┌─────────▼──────────┐
         │   RAG System       │     │   Direct Query     │
         │                    │     │                    │
         │ ┌────────────────┐ │     │ ┌────────────────┐ │
         │ │ Query Embed.   │ │     │ │ System Prompt  │ │
         │ └────────────────┘ │     │ └────────────────┘ │
         │         ▼          │     │         ▼          │
         │ ┌────────────────┐ │     │ ┌────────────────┐ │
         │ │ Vector Search  │ │     │ │ Generate Reply │ │
         │ └────────────────┘ │     │ └────────────────┘ │
         │         ▼          │     └──────────┬─────────┘
         │ ┌────────────────┐ │                │
         │ │ Format Context │ │                │
         │ └────────────────┘ │                │
         │         ▼          │                │
         │ ┌────────────────┐ │                │
         │ │ Generate Reply │ │                │
         │ └────────────────┘ │                │
         └─────────┬──────────┘                │
                   │                           │
                   └───────────┬───────────────┘
                               ▼
         ┌─────────────────────────────────────────┐
         │      Azure OpenAI Service               │
         │  ┌─────────────┐   ┌──────────────┐    │
         │  │ Chat Model  │   │ Embeddings   │    │
         │  │ (GPT-3.5/4) │   │ (ada-002)    │    │
         │  └─────────────┘   └──────────────┘    │
         └─────────────────────────────────────────┘

         ┌─────────────────────────────────────────┐
         │      Vector Database                    │
         │  ┌─────────────┐   ┌──────────────┐    │
         │  │  Pinecone   │   │  Weaviate    │    │
         │  │  (Cloud)    │   │  (Local/Cloud)    │
         │  └─────────────┘   └──────────────┘    │
         └─────────────────────────────────────────┘
```

## Component Details

### 1. Configuration Layer (`src/config.py`)

**Purpose**: Centralized configuration management

**Responsibilities**:
- Load environment variables
- Validate required settings
- Provide typed configuration objects

**Configuration Groups**:
- `AzureOpenAIConfig`: Azure OpenAI settings
- `VectorDBConfig`: Vector database settings
- `ChatbotConfig`: Chatbot behavior settings

### 2. Azure OpenAI Client (`src/azure_openai_client.py`)

**Purpose**: Interface to Azure OpenAI services

**Key Methods**:
- `generate_completion()`: Chat completion
- `generate_embeddings()`: Text embeddings
- `query_with_context()`: Query with RAG context
- `direct_query()`: Direct query without context

**Features**:
- Handles authentication
- Manages API calls
- Provides system prompts for Velero domain

### 3. Document Loader (`src/document_loader.py`)

**Purpose**: Load and process repository documents

**Process Flow**:
```
Repository Files
    ↓
Load Markdown Files
    ↓
Split into Chunks (with overlap)
    ↓
Prepare for Indexing
    ↓
Return Document Chunks
```

**Features**:
- Loads from multiple sources (docs, README, etc.)
- Smart chunking with paragraph awareness
- Maintains metadata (source, type, chunk ID)

### 4. Vector Database (`src/vector_db.py`)

**Purpose**: Abstract vector database operations

**Architecture**:
```
VectorDBInterface (Abstract)
    ├── PineconeDB (Implementation)
    └── WeaviateDB (Implementation)
```

**Operations**:
- `create_index()`: Initialize vector index
- `index_documents()`: Store embeddings
- `search()`: Similarity search
- `index_exists()`: Check index status

**Design Pattern**: Strategy pattern for database selection

### 5. RAG System (`src/rag_system.py`)

**Purpose**: Implement Retrieval-Augmented Generation

**RAG Pipeline**:
```
User Query
    ↓
Generate Query Embedding
    ↓
Search Vector Database (Top-K)
    ↓
Retrieved Documents
    ↓
Format as Context
    ↓
Query + Context → Azure OpenAI
    ↓
Answer + Sources
```

**Features**:
- Semantic search using embeddings
- Context formatting
- Source attribution
- Batch embedding generation for indexing

### 6. Chatbot (`src/chatbot.py`)

**Purpose**: Main orchestration and business logic

**Decision Flow**:
```
User Query
    ↓
Is Valid? ────No───→ Return Error
    ↓ Yes
Is Velero-related? ──No───→ Return Scope Message
    ↓ Yes
RAG Enabled?
    ↓ Yes                ↓ No
RAG Query            Direct Query
    ↓                    ↓
Return Answer + Sources
```

**Key Features**:
- Query validation
- Domain restriction (Velero-related)
- Graceful fallback
- Status reporting

### 7. CLI Interface (`cli.py`)

**Purpose**: User interaction layer

**Commands**:
- `index`: Index repository documents
- `chat`: Interactive or single-query mode
- `status`: Show system status

**Features**:
- Rich formatting (colors, panels, markdown)
- Progress indicators
- Error handling
- Configuration file support

## Data Flow

### Indexing Flow

```
1. User runs: python cli.py index
    ↓
2. Document Loader loads and chunks documents
    ↓
3. Azure OpenAI generates embeddings (batch)
    ↓
4. Vector DB stores embeddings with metadata
    ↓
5. Index ready for queries
```

### Query Flow (RAG Mode)

```
1. User asks question
    ↓
2. Chatbot validates query
    ↓
3. RAG System generates query embedding
    ↓
4. Vector DB returns Top-K similar documents
    ↓
5. RAG System formats context from documents
    ↓
6. Azure OpenAI generates answer with context
    ↓
7. Return answer + sources to user
```

### Query Flow (Direct Mode)

```
1. User asks question
    ↓
2. Chatbot validates query
    ↓
3. Azure OpenAI generates answer (with Velero system prompt)
    ↓
4. Return answer to user
```

## Design Decisions

### 1. Modular Architecture

**Rationale**: 
- Easy to extend (add new vector databases)
- Testable components
- Clear separation of concerns

### 2. Abstract Vector Database Interface

**Rationale**:
- Support multiple vector databases
- Easy to add new databases
- Decouples business logic from database choice

### 3. Dual Mode Operation

**Rationale**:
- RAG provides better answers with sources
- Direct mode useful for quick setup
- Graceful fallback if RAG fails

### 4. Chunking with Overlap

**Rationale**:
- Maintains context across chunk boundaries
- Improves retrieval quality
- Prevents information loss at boundaries

### 5. Domain Validation

**Rationale**:
- Keeps chatbot focused on Velero
- Prevents off-topic queries
- Better user experience

### 6. Configuration via Environment

**Rationale**:
- 12-factor app principles
- Easy deployment configuration
- Secure credential management

## Extension Points

### Adding a New Vector Database

1. Implement `VectorDBInterface`
2. Add to `get_vector_db()` factory
3. Add configuration options

Example:
```python
class ChromaDB(VectorDBInterface):
    def create_index(self, dimension):
        # Implementation
        pass
    # ... other methods
```

### Adding a Web Interface

1. Create web app (Flask/FastAPI)
2. Import `VeleroChatbot`
3. Expose query endpoint

Example:
```python
@app.route('/api/query', methods=['POST'])
def query():
    question = request.json['question']
    result = chatbot.query(question)
    return jsonify(result)
```

### Adding Conversation History

1. Extend `VeleroChatbot` with session management
2. Store conversation context
3. Pass history to OpenAI

### Adding Response Caching

1. Add cache layer (Redis/Memory)
2. Hash queries
3. Return cached responses for duplicates

## Performance Considerations

### Indexing
- **Time**: 2-5 minutes for ~100 documents
- **Cost**: ~$0.01-0.05 for embeddings (one-time)
- **Optimization**: Batch embedding generation

### Query (RAG Mode)
- **Latency**: 2-5 seconds
  - Embedding: ~0.5s
  - Vector search: ~0.1s
  - LLM generation: 1-4s
- **Cost**: ~$0.001-0.01 per query
- **Optimization**: Reduce `TOP_K_RESULTS`

### Query (Direct Mode)
- **Latency**: 1-3 seconds
- **Cost**: ~$0.001-0.005 per query
- **Optimization**: Use GPT-3.5 instead of GPT-4

## Security

### Credentials
- Environment variables (not hardcoded)
- `.env` excluded from git
- Separate keys for dev/prod

### Input Validation
- Query sanitization
- Domain validation (Velero-only)
- Error handling

### Rate Limiting
- Consider adding for production
- Azure OpenAI has built-in limits

### Data Privacy
- Repository content indexed in vector DB
- Queries sent to Azure OpenAI
- No PII should be in documents

## Scalability

### Current Design
- Single-user CLI
- Stateless operation
- No persistent sessions

### For Production
- Add caching layer
- Implement load balancing
- Use managed vector DB
- Monitor costs and usage

## Testing Strategy

### Unit Tests
- Configuration validation
- Document chunking logic
- Vector DB interface

### Integration Tests
- Azure OpenAI connection
- Vector DB operations
- End-to-end query flow

### Manual Testing
- Use example queries
- Verify answer quality
- Check source attribution

## Monitoring

### Key Metrics
- Query latency
- Success/failure rate
- Cost per query
- Vector DB performance

### Logging
- Query logs
- Error logs
- Performance metrics

## Future Enhancements

1. **Web UI**: Browser-based interface
2. **Conversation History**: Multi-turn conversations
3. **Hybrid Search**: Combine keyword + semantic
4. **Re-ranking**: Improve retrieval quality
5. **Multi-language**: Support for multiple languages
6. **Analytics Dashboard**: Usage and performance metrics
7. **Feedback Loop**: Learn from user feedback
8. **Streaming Responses**: Real-time token streaming
