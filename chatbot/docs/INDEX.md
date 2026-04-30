# Velero Chatbot Documentation

Welcome to the Velero Chatbot documentation! This chatbot helps users interact with Velero documentation using AI-powered question answering.

## 📚 Documentation Index

### Getting Started
- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[Configuration Guide](CONFIGURATION.md)** - Detailed configuration options
- **[Example Queries](../examples/example_queries.md)** - Sample questions to try

### Understanding the System
- **[Architecture](ARCHITECTURE.md)** - System design and components
- **[README](../README.md)** - Complete feature overview and usage

### Deployment
- **[Deployment Guide](DEPLOYMENT.md)** - Local, Docker, and cloud deployment

## 🎯 Choose Your Path

### I want to try it quickly
→ Follow the [Quick Start Guide](QUICKSTART.md)

### I want to understand how it works
→ Read the [Architecture Guide](ARCHITECTURE.md)

### I want to deploy in production
→ Check the [Deployment Guide](DEPLOYMENT.md)

### I want to configure advanced features
→ See the [Configuration Guide](CONFIGURATION.md)

## 📖 What is the Velero Chatbot?

The Velero Chatbot is an AI-powered assistant that helps users:
- Get instant answers about Velero
- Find relevant documentation quickly
- Understand Velero concepts and usage
- Troubleshoot common issues

## 🔑 Key Features

### Dual Query Modes

**RAG Mode** (Recommended):
- Uses Retrieval-Augmented Generation
- Searches Velero documentation
- Provides source attribution
- More accurate and contextual

**Direct Mode**:
- Uses Azure OpenAI directly
- No vector database required
- Quick setup
- Good for general questions

### Supported Vector Databases
- **Pinecone**: Cloud-based, easy setup
- **Weaviate**: Self-hosted or cloud

### Interactive CLI
- Rich formatting with colors
- Markdown support
- Source attribution
- Easy to use

## 🚀 Quick Start

```bash
# 1. Install dependencies
cd chatbot
pip install -r requirements.txt

# 2. Configure
cp config/.env.example config/.env
# Edit config/.env with your Azure OpenAI credentials

# 3. (Optional) Index for RAG
python cli.py index --env-file config/.env

# 4. Start chatting
python cli.py chat --env-file config/.env
```

## 📋 Prerequisites

**Required**:
- Python 3.8+
- Azure OpenAI API access

**Optional (for RAG)**:
- Pinecone account OR
- Weaviate instance (local or cloud)

## 💡 Common Use Cases

### Learning Velero
```
You: What is Velero and what can it do?
You: How does Velero differ from other backup solutions?
```

### Installation and Setup
```
You: How do I install Velero on AWS?
You: What are the prerequisites for Velero?
```

### Operations
```
You: How do I create a backup?
You: How can I schedule automatic backups?
You: What's the process for restoring a backup?
```

### Troubleshooting
```
You: Why is my backup failing?
You: How do I debug Velero issues?
```

## 🏗️ Architecture Overview

```
User ─→ CLI ─→ Chatbot ─→ RAG System ─→ Vector DB
                    │                      ↓
                    │                  Retrieved Docs
                    ↓                      ↓
              Azure OpenAI ←───────────────┘
```

**Components**:
- **CLI**: User interface
- **Chatbot**: Orchestration and routing
- **RAG System**: Document retrieval
- **Azure OpenAI**: Language understanding and generation
- **Vector DB**: Document storage and search

## 🔧 Configuration

Key configuration options:

```bash
# Azure OpenAI (Required)
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo

# RAG Mode (Optional)
ENABLE_RAG=true
VECTOR_DB_TYPE=pinecone
PINECONE_API_KEY=your_key

# Tuning
CHUNK_SIZE=1000
TOP_K_RESULTS=5
TEMPERATURE=0.7
```

See [Configuration Guide](CONFIGURATION.md) for details.

## 🐳 Deployment Options

### Local Development
```bash
./setup.sh
python cli.py chat --env-file config/.env
```

### Docker
```bash
docker build -t velero-chatbot .
docker run -it --env-file config/.env velero-chatbot chat
```

### Kubernetes
```bash
kubectl apply -f k8s-deployment.yaml
```

See [Deployment Guide](DEPLOYMENT.md) for detailed instructions.

## 📊 Performance

**Indexing**:
- Time: 2-5 minutes for ~100 documents
- Cost: ~$0.01-0.05 (one-time)

**Queries (RAG)**:
- Latency: 2-5 seconds
- Cost: ~$0.001-0.01 per query

**Queries (Direct)**:
- Latency: 1-3 seconds
- Cost: ~$0.001-0.005 per query

## 🔒 Security

- Environment-based configuration
- No hardcoded credentials
- Input validation
- Domain restriction (Velero-only queries)

See [Deployment Guide](DEPLOYMENT.md) for security best practices.

## 🧪 Testing

### Manual Testing

1. **Status Check**:
   ```bash
   python cli.py status --env-file config/.env
   ```

2. **Sample Queries**:
   ```bash
   python cli.py chat --env-file config/.env --query "What is Velero?"
   ```

3. **Interactive Mode**:
   ```bash
   python cli.py chat --env-file config/.env
   ```

### Testing Examples

See [Example Queries](../examples/example_queries.md) for comprehensive test cases.

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. **Additional Vector Databases**: ChromaDB, Qdrant, etc.
2. **Web Interface**: React/Vue frontend
3. **Advanced RAG**: Re-ranking, hybrid search
4. **Caching**: Response caching layer
5. **Analytics**: Usage tracking and metrics

## 📝 Documentation Structure

```
chatbot/
├── README.md                 # Main overview
├── docs/
│   ├── INDEX.md             # This file
│   ├── QUICKSTART.md        # 5-minute setup
│   ├── CONFIGURATION.md     # Detailed config
│   ├── ARCHITECTURE.md      # System design
│   └── DEPLOYMENT.md        # Production guide
├── examples/
│   └── example_queries.md   # Sample questions
└── config/
    └── .env.example         # Config template
```

## 🆘 Getting Help

### Documentation Issues
- Check [Troubleshooting](../README.md#troubleshooting) section
- Review [Configuration Guide](CONFIGURATION.md)
- See [Example Queries](../examples/example_queries.md)

### Chatbot Issues
- Verify configuration with `status` command
- Check logs for errors
- Review [Architecture](ARCHITECTURE.md) for understanding

### General Velero Questions
- [Velero Documentation](https://velero.io/docs/)
- [Velero Slack Channel](https://kubernetes.slack.com/messages/velero)
- [GitHub Issues](https://github.com/vmware-tanzu/velero/issues)

## 🔗 Useful Links

- [Velero Project](https://velero.io/)
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- [Pinecone](https://www.pinecone.io/)
- [Weaviate](https://weaviate.io/)

## 📄 License

This chatbot is part of the Velero project and follows the same license (Apache 2.0).

## 🎉 Next Steps

1. **New Users**: Start with [Quick Start Guide](QUICKSTART.md)
2. **Developers**: Read [Architecture Guide](ARCHITECTURE.md)
3. **Operators**: Check [Deployment Guide](DEPLOYMENT.md)
4. **Contributors**: Review system components and extend functionality

## 💬 Questions?

- Open an issue in the Velero repository
- Ask in the [#velero Slack channel](https://kubernetes.slack.com/messages/velero)
- Refer to specific documentation sections above

---

**Happy Chatting! 🚀**
