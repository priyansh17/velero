# Quick Start Guide

This guide will help you get started with the Velero Chatbot in 5 minutes.

## Step 1: Install Dependencies

```bash
cd chatbot
pip install -r requirements.txt
```

## Step 2: Configure Azure OpenAI

1. Get your Azure OpenAI credentials:
   - API Key
   - Endpoint URL
   - Deployment names

2. Copy and edit the configuration:
   ```bash
   cp config/.env.example config/.env
   nano config/.env  # or use your preferred editor
   ```

3. Update these required fields:
   ```bash
   AZURE_OPENAI_API_KEY=your_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
   ```

## Step 3: Choose Your Mode

### Option A: Quick Start (No RAG)

For immediate use without setting up a vector database:

```bash
# In config/.env
ENABLE_RAG=false
```

Then start chatting:
```bash
python cli.py chat --env-file config/.env
```

### Option B: Full Setup (With RAG)

For better, context-aware answers:

1. **Setup Pinecone** (easiest):
   - Sign up at [pinecone.io](https://www.pinecone.io/)
   - Create a project and get your API key
   - Add to `config/.env`:
     ```bash
     PINECONE_API_KEY=your_key
     PINECONE_ENVIRONMENT=us-east-1-aws
     ENABLE_RAG=true
     VECTOR_DB_TYPE=pinecone
     ```

2. **Index the repository**:
   ```bash
   python cli.py index --env-file config/.env
   ```
   This takes 2-5 minutes depending on your connection.

3. **Start chatting**:
   ```bash
   python cli.py chat --env-file config/.env
   ```

## Step 4: Ask Questions!

```
You: What is Velero?
You: How do I create a backup?
You: What cloud providers are supported?
```

Type `exit` or `quit` to end the session.

## Example Queries

- "How do I install Velero?"
- "What are the differences between backups and snapshots?"
- "How can I schedule automatic backups?"
- "What's the process for restoring a backup?"
- "How do I migrate a cluster to a different cloud provider?"

## Troubleshooting

### Can't connect to Azure OpenAI
- Check your API key and endpoint
- Verify your deployment names are correct
- Ensure you have access to the Azure OpenAI service

### "No module named 'X'"
```bash
pip install -r requirements.txt
```

### RAG not working
- Make sure you ran the `index` command first
- Verify your vector database credentials
- Check status: `python cli.py status --env-file config/.env`

## Next Steps

- Read the full [README.md](README.md) for detailed configuration
- Explore advanced options in [config/.env.example](config/.env.example)
- Check out [examples/](examples/) for sample queries
