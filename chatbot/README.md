# Velero Chatbot

An intelligent chatbot for the Velero project that can answer queries about Velero using either Retrieval-Augmented Generation (RAG) or direct Azure OpenAI integration.

## Features

- **Dual Query Modes:**
  - **RAG Mode:** Retrieves relevant documentation and provides context-aware answers using a vector database
  - **Direct Mode:** Answers queries directly using Azure OpenAI models
  
- **Vector Database Support:**
  - Pinecone (serverless vector database)
  - Weaviate (open-source vector database)
  
- **Document Processing:**
  - Automatically indexes Velero documentation
  - Processes README files and repository content
  - Intelligent chunking with overlap for better context
  
- **Interactive CLI:**
  - User-friendly command-line interface
  - Rich formatting with markdown support
  - Source attribution for RAG responses

## Prerequisites

### Required

- Python 3.8 or higher
- Azure OpenAI API access with:
  - Chat completion deployment (e.g., GPT-4, GPT-3.5-turbo)
  - Text embedding deployment (e.g., text-embedding-ada-002)

### Optional (for RAG mode)

Choose one:
- **Pinecone:** Free tier available at [pinecone.io](https://www.pinecone.io/)
- **Weaviate:** Can run locally with Docker or use cloud service

## Installation

### 1. Clone the Repository

```bash
cd /path/to/velero
cd chatbot
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

### 1. Create Environment File

Copy the example configuration:

```bash
cp config/.env.example config/.env
```

### 2. Configure Azure OpenAI

Edit `config/.env` and set your Azure OpenAI credentials:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_chat_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your_embedding_deployment_name
```

To get these values:
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Under "Keys and Endpoint", copy the key and endpoint
4. Under "Model deployments", note your deployment names

### 3. Configure Vector Database (for RAG mode)

#### Option A: Using Pinecone

```bash
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=velero-docs

# Set vector DB type
VECTOR_DB_TYPE=pinecone
ENABLE_RAG=true
```

To get Pinecone credentials:
1. Sign up at [pinecone.io](https://www.pinecone.io/)
2. Create a new project
3. Copy your API key from the project settings

#### Option B: Using Weaviate

For local Weaviate instance:

```bash
# Start Weaviate with Docker
docker run -d -p 8080:8080 semitechnologies/weaviate:latest

# Configure in .env
WEAVIATE_URL=http://localhost:8080
VECTOR_DB_TYPE=weaviate
ENABLE_RAG=true
```

For cloud Weaviate:

```bash
WEAVIATE_URL=https://your-cluster.weaviate.network
WEAVIATE_API_KEY=your_weaviate_api_key
VECTOR_DB_TYPE=weaviate
ENABLE_RAG=true
```

### 4. Disable RAG (Optional)

To use direct Azure OpenAI queries without RAG:

```bash
ENABLE_RAG=false
```

## Usage

### Index Repository Documents (First Time Setup)

Before using RAG mode, you need to index the repository documents:

```bash
python cli.py index --env-file config/.env
```

This will:
1. Load all markdown files from the repository
2. Generate embeddings using Azure OpenAI
3. Store them in your configured vector database

**Note:** This is a one-time operation (or when you want to refresh the index).

### Interactive Chat Mode

Start an interactive chat session:

```bash
python cli.py chat --env-file config/.env
```

Example interaction:

```
Velero Chatbot
Initializing...

╭─────────── Chatbot Status ───────────╮
│ RAG Mode: Enabled                     │
│ Vector DB: pinecone                   │
│ Index Ready: Yes                      │
╰───────────────────────────────────────╯

Type your questions about Velero. Type 'exit' or 'quit' to end the session.

You: How do I backup a Kubernetes cluster with Velero?

Thinking...

Assistant
╭─────────── Answer (RAG) ──────────────╮
│ To backup a Kubernetes cluster with   │
│ Velero, follow these steps:           │
│                                        │
│ 1. Install Velero...                  │
│ [detailed answer with context]        │
╰────────────────────────────────────────╯

╭────────────── Sources ─────────────────╮
│ • site/content/docs/backup.md (0.92)  │
│ • README.md (0.85)                     │
╰────────────────────────────────────────╯
```

### Single Query Mode

Ask a single question without interactive mode:

```bash
python cli.py chat --env-file config/.env --query "What is Velero?"
```

### Hide Sources

To hide source attribution:

```bash
python cli.py chat --env-file config/.env --no-sources
```

### Check Status

Check the chatbot's configuration and status:

```bash
python cli.py status --env-file config/.env
```

## Advanced Configuration

### Tuning RAG Performance

Edit `config/.env` to adjust these parameters:

```bash
# Chunk size for document splitting (in characters)
CHUNK_SIZE=1000

# Overlap between chunks (helps maintain context)
CHUNK_OVERLAP=200

# Number of relevant documents to retrieve
TOP_K_RESULTS=5

# Model temperature (0.0 = deterministic, 1.0 = creative)
TEMPERATURE=0.7

# Maximum tokens in response
MAX_TOKENS=1000
```

### Custom Repository Paths

If running from a different location:

```bash
# Path to repository root (relative to chatbot directory)
REPO_PATH=../

# Path to documentation directory
DOCS_PATH=../site/content
```

## Troubleshooting

### "No module named 'pinecone'" or similar

Make sure you've installed all dependencies:

```bash
pip install -r requirements.txt
```

### "AZURE_OPENAI_API_KEY is required"

Ensure your `config/.env` file is properly configured with Azure OpenAI credentials.

### "Index not found" or "Vector database not ready"

Run the indexing command first:

```bash
python cli.py index --env-file config/.env
```

### RAG returns "No relevant context found"

This might happen if:
1. The index is empty - run `index` command
2. Your query is too specific - try rephrasing
3. The topic isn't covered in the documentation

### Connection errors to vector database

**Pinecone:**
- Verify your API key and environment are correct
- Check your internet connection
- Ensure your Pinecone project is active

**Weaviate:**
- If running locally, ensure Docker container is running: `docker ps`
- Check the URL is correct (default: `http://localhost:8080`)
- For cloud instances, verify your API key

## Architecture

### Components

1. **Configuration Module (`src/config.py`):**
   - Loads and validates environment configuration
   - Manages Azure OpenAI and vector DB settings

2. **Azure OpenAI Client (`src/azure_openai_client.py`):**
   - Handles chat completions
   - Generates embeddings
   - Manages prompts and context

3. **Document Loader (`src/document_loader.py`):**
   - Loads markdown files from repository
   - Chunks documents with overlap
   - Prepares documents for indexing

4. **Vector Database (`src/vector_db.py`):**
   - Abstract interface for vector databases
   - Pinecone implementation
   - Weaviate implementation

5. **RAG System (`src/rag_system.py`):**
   - Retrieves relevant documents
   - Formats context for queries
   - Generates context-aware answers

6. **Chatbot (`src/chatbot.py`):**
   - Main orchestration logic
   - Query routing (RAG vs. Direct)
   - Domain validation (Velero-related queries)

7. **CLI Interface (`cli.py`):**
   - Interactive and single-query modes
   - Rich formatting and user experience
   - Index and status commands

### Data Flow

**RAG Mode:**
```
User Query
    ↓
Generate Query Embedding (Azure OpenAI)
    ↓
Search Vector Database (Pinecone/Weaviate)
    ↓
Retrieve Top-K Relevant Documents
    ↓
Format Context from Documents
    ↓
Generate Answer with Context (Azure OpenAI)
    ↓
Return Answer + Sources
```

**Direct Mode:**
```
User Query
    ↓
Validate Query (Velero-related)
    ↓
Generate Answer (Azure OpenAI)
    ↓
Return Answer
```

## Production Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "cli.py"]
CMD ["chat", "--env-file", "config/.env"]
```

Build and run:

```bash
docker build -t velero-chatbot .
docker run -it --env-file config/.env velero-chatbot
```

### Environment Variables

For production, use environment variables instead of `.env` file:

```bash
export AZURE_OPENAI_API_KEY="your_key"
export AZURE_OPENAI_ENDPOINT="your_endpoint"
# ... other variables

python cli.py chat
```

### Web Interface (Future Enhancement)

While the current implementation provides a CLI interface, you can extend it with a web interface using frameworks like:
- **Flask/FastAPI:** For REST API
- **Streamlit:** For quick web UI
- **Gradio:** For ML-focused interface

Example structure:
```python
# web_app.py
from flask import Flask, request, jsonify
from src.config import Config
from src.chatbot import VeleroChatbot

app = Flask(__name__)
chatbot = VeleroChatbot(Config())

@app.route('/query', methods=['POST'])
def query():
    question = request.json.get('question')
    result = chatbot.query(question)
    return jsonify(result)
```

## Security Considerations

1. **API Keys:**
   - Never commit `.env` files with real credentials
   - Use environment variables in production
   - Rotate keys regularly

2. **Input Validation:**
   - The chatbot validates queries are Velero-related
   - Additional sanitization may be needed for production

3. **Rate Limiting:**
   - Consider implementing rate limiting for API calls
   - Monitor Azure OpenAI usage

4. **Data Privacy:**
   - Repository content is indexed in vector database
   - Ensure compliance with data handling policies

## Cost Optimization

### Azure OpenAI Costs

- **Embeddings:** ~$0.0001 per 1K tokens
- **Chat Completions:** Varies by model (GPT-3.5 vs GPT-4)

Tips:
- Use GPT-3.5-turbo for cost-effective responses
- Cache common queries
- Adjust `TOP_K_RESULTS` to retrieve fewer documents

### Vector Database Costs

**Pinecone:**
- Free tier: 1 index, 100K vectors
- Paid: Starts at $70/month for more capacity

**Weaviate:**
- Self-hosted: Free (infrastructure costs only)
- Cloud: Pricing varies

## Contributing

Contributions are welcome! Areas for improvement:

1. **Additional Vector Databases:** Add support for ChromaDB, Qdrant, etc.
2. **Web Interface:** Build a web UI for the chatbot
3. **Advanced RAG:** Implement re-ranking, hybrid search
4. **Caching:** Add response caching
5. **Analytics:** Track query patterns and performance

## License

This chatbot is part of the Velero project and follows the same license (Apache 2.0).

## Support

For issues and questions:
- Open an issue in the Velero repository
- Ask on the [#velero Slack channel](https://kubernetes.slack.com/messages/velero)
- Refer to [Velero documentation](https://velero.io/docs/)

## Acknowledgments

- Built for the [Velero project](https://velero.io/)
- Uses [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- Supports [Pinecone](https://www.pinecone.io/) and [Weaviate](https://weaviate.io/)
