# Configuration Guide

Complete guide to configuring the Velero Chatbot.

## Configuration File

The chatbot uses environment variables loaded from a `.env` file. Copy the example:

```bash
cp config/.env.example config/.env
```

## Required Configuration

### Azure OpenAI Settings

These are **required** for the chatbot to work:

```bash
# Your Azure OpenAI API key
AZURE_OPENAI_API_KEY=sk-...

# Your Azure OpenAI endpoint URL
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/

# The name of your chat completion deployment
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo

# API version to use
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# The name of your embedding model deployment (required for RAG)
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
```

#### How to Get Azure OpenAI Credentials

1. **Create Azure OpenAI Resource:**
   - Go to [Azure Portal](https://portal.azure.com)
   - Create a new "Azure OpenAI" resource
   - Note the resource name

2. **Deploy Models:**
   - In your Azure OpenAI resource, go to "Model deployments"
   - Deploy a chat model (e.g., `gpt-35-turbo` or `gpt-4`)
   - Deploy an embedding model (e.g., `text-embedding-ada-002`)
   - Note the deployment names

3. **Get API Key:**
   - Go to "Keys and Endpoint" in your resource
   - Copy "Key 1" or "Key 2"
   - Copy the "Endpoint" URL

## Optional: RAG Configuration

To enable RAG (Retrieval-Augmented Generation), you need a vector database.

### Enable/Disable RAG

```bash
# Enable RAG mode (requires vector database)
ENABLE_RAG=true

# Or disable for direct queries only
ENABLE_RAG=false
```

### Vector Database Type

```bash
# Choose: pinecone or weaviate
VECTOR_DB_TYPE=pinecone
```

### Pinecone Configuration

If using Pinecone (`VECTOR_DB_TYPE=pinecone`):

```bash
# Pinecone API key
PINECONE_API_KEY=your-api-key

# Pinecone environment (e.g., us-east-1-aws)
PINECONE_ENVIRONMENT=us-east-1-aws

# Index name (will be created if doesn't exist)
PINECONE_INDEX_NAME=velero-docs
```

**Getting Pinecone Credentials:**

1. Sign up at [pinecone.io](https://www.pinecone.io/)
2. Create a new project
3. Go to "API Keys" and copy your key
4. Note your environment (shown in the dashboard)

### Weaviate Configuration

If using Weaviate (`VECTOR_DB_TYPE=weaviate`):

```bash
# Weaviate URL
WEAVIATE_URL=http://localhost:8080

# Weaviate API key (optional, for cloud instances)
WEAVIATE_API_KEY=your-api-key
```

**Local Weaviate Setup:**

```bash
# Using Docker
docker run -d \
  -p 8080:8080 \
  --name weaviate \
  semitechnologies/weaviate:latest

# Then use
WEAVIATE_URL=http://localhost:8080
```

**Cloud Weaviate:**

1. Sign up at [Weaviate Cloud Services](https://console.weaviate.cloud/)
2. Create a cluster
3. Copy the cluster URL and API key

## RAG Tuning Parameters

### Chunk Size

Size of document chunks for indexing (in characters):

```bash
CHUNK_SIZE=1000
```

- **Smaller (500-800):** More precise matches, more chunks
- **Larger (1200-1500):** More context, fewer chunks
- **Default (1000):** Good balance

### Chunk Overlap

Overlap between consecutive chunks (in characters):

```bash
CHUNK_OVERLAP=200
```

- **Purpose:** Maintains context across chunk boundaries
- **Typical range:** 100-300
- **Default (200):** Recommended for most cases

### Top K Results

Number of relevant documents to retrieve:

```bash
TOP_K_RESULTS=5
```

- **Smaller (3):** Faster, more focused
- **Larger (7-10):** More comprehensive, slower
- **Default (5):** Good balance

## Model Parameters

### Temperature

Controls randomness in responses (0.0 to 1.0):

```bash
TEMPERATURE=0.7
```

- **0.0-0.3:** Deterministic, factual
- **0.4-0.6:** Balanced
- **0.7-1.0:** Creative, varied
- **Default (0.7):** Good for conversational responses

### Max Tokens

Maximum length of generated responses:

```bash
MAX_TOKENS=1000
```

- **Smaller (500):** Concise answers, lower cost
- **Larger (1500-2000):** Detailed answers, higher cost
- **Default (1000):** Suitable for most queries

## Repository Paths

Paths relative to the chatbot directory:

```bash
# Repository root
REPO_PATH=../

# Documentation directory
DOCS_PATH=../site/content
```

**When to Change:**
- Running chatbot from different location
- Custom repository structure
- Testing with different documentation

## Complete Example Configurations

### Minimal Setup (No RAG)

```bash
# Azure OpenAI (Required)
AZURE_OPENAI_API_KEY=sk-xxx
AZURE_OPENAI_ENDPOINT=https://my-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002

# Disable RAG
ENABLE_RAG=false

# Model settings
TEMPERATURE=0.7
MAX_TOKENS=1000

# Paths
REPO_PATH=../
DOCS_PATH=../site/content
```

### Full Setup with Pinecone

```bash
# Azure OpenAI (Required)
AZURE_OPENAI_API_KEY=sk-xxx
AZURE_OPENAI_ENDPOINT=https://my-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002

# Pinecone
PINECONE_API_KEY=xxx
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=velero-docs

# Enable RAG
VECTOR_DB_TYPE=pinecone
ENABLE_RAG=true
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5

# Model settings
TEMPERATURE=0.7
MAX_TOKENS=1000

# Paths
REPO_PATH=../
DOCS_PATH=../site/content
```

### Full Setup with Local Weaviate

```bash
# Azure OpenAI (Required)
AZURE_OPENAI_API_KEY=sk-xxx
AZURE_OPENAI_ENDPOINT=https://my-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002

# Weaviate (Local)
WEAVIATE_URL=http://localhost:8080

# Enable RAG
VECTOR_DB_TYPE=weaviate
ENABLE_RAG=true
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5

# Model settings
TEMPERATURE=0.7
MAX_TOKENS=1000

# Paths
REPO_PATH=../
DOCS_PATH=../site/content
```

## Validation

After configuration, test your setup:

```bash
# Check status
python cli.py status --env-file config/.env

# Expected output:
# ✓ Azure OpenAI: Configured
# ✓ RAG Mode: Enabled
# ✓ Vector DB: pinecone
# ✓ Index Ready: Yes (after indexing)
```

## Security Best Practices

1. **Never commit `.env` files:**
   ```bash
   # Add to .gitignore
   config/.env
   ```

2. **Use different keys for dev/prod:**
   - Separate Azure OpenAI resources
   - Separate vector DB indexes

3. **Rotate keys regularly:**
   - Azure: Regenerate keys periodically
   - Vector DB: Update API keys

4. **Use environment variables in production:**
   ```bash
   export AZURE_OPENAI_API_KEY="xxx"
   python cli.py chat
   ```

## Troubleshooting

### Configuration Not Loading

```bash
# Explicitly specify config file
python cli.py chat --env-file config/.env

# Check file exists
ls -la config/.env

# Check file format (no quotes around values)
cat config/.env
```

### Invalid Configuration

```bash
# Test configuration
python -c "from src.config import Config; c = Config(); c.validate(); print('OK')"
```

### Vector Database Connection Issues

```bash
# Test Pinecone connection
python -c "from pinecone import Pinecone; pc = Pinecone(api_key='YOUR_KEY'); print(pc.list_indexes())"

# Test Weaviate connection
python -c "import weaviate; client = weaviate.Client('http://localhost:8080'); print(client.is_ready())"
```
