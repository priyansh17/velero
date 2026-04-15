# Velero Chatbot Integration

This document describes the Velero Chatbot integration in the Velero repository.

## Overview

The Velero Chatbot is an AI-powered assistant that helps users interact with Velero documentation and get answers to their questions. It uses Azure OpenAI and optional Retrieval-Augmented Generation (RAG) for context-aware responses.

## Location

The chatbot is located in the `chatbot/` directory at the root of the repository:

```
velero/
├── chatbot/              # Chatbot implementation
│   ├── README.md         # Main documentation
│   ├── cli.py            # Command-line interface
│   ├── requirements.txt  # Python dependencies
│   ├── setup.sh          # Setup script
│   ├── config/           # Configuration
│   ├── docs/             # Documentation
│   ├── examples/         # Example queries
│   └── src/              # Source code
├── cmd/                  # Velero CLI (Go)
├── pkg/                  # Velero packages (Go)
├── site/                 # Documentation site
└── ...
```

## Features

### Core Capabilities

1. **Dual Query Modes**:
   - **RAG Mode**: Retrieves relevant documentation before answering
   - **Direct Mode**: Uses Azure OpenAI directly

2. **Vector Database Support**:
   - Pinecone (cloud-based)
   - Weaviate (self-hosted or cloud)

3. **Document Indexing**:
   - Automatically indexes Velero documentation from `site/content/`
   - Processes README files and repository content
   - Smart chunking for better retrieval

4. **Interactive CLI**:
   - User-friendly command-line interface
   - Rich formatting with markdown support
   - Source attribution for answers

### What It Does

The chatbot helps users:
- Get instant answers about Velero
- Find relevant documentation quickly
- Understand Velero concepts and usage
- Troubleshoot common issues

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI API access
- (Optional) Pinecone or Weaviate account for RAG mode

### Installation

```bash
cd chatbot
pip install -r requirements.txt

# Configure
cp config/.env.example config/.env
# Edit config/.env with your credentials

# Index (for RAG mode)
python cli.py index --env-file config/.env

# Start chatting
python cli.py chat --env-file config/.env
```

For detailed instructions, see [chatbot/README.md](README.md).

## Architecture

The chatbot is implemented in Python and consists of:

- **Configuration Module**: Manages environment-based configuration
- **Azure OpenAI Client**: Handles API calls to Azure OpenAI
- **Document Loader**: Loads and processes Velero documentation
- **Vector Database**: Stores and searches document embeddings
- **RAG System**: Implements Retrieval-Augmented Generation
- **Chatbot Controller**: Main orchestration logic
- **CLI Interface**: User interaction layer

See [chatbot/docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

## Documentation

Comprehensive documentation is available in the `chatbot/docs/` directory:

- **[README.md](README.md)**: Main overview and usage
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)**: 5-minute setup guide
- **[docs/CONFIGURATION.md](docs/CONFIGURATION.md)**: Detailed configuration
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**: System design
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)**: Production deployment
- **[examples/example_queries.md](examples/example_queries.md)**: Sample questions

## Integration with Velero

### Documentation Integration

The chatbot automatically indexes documentation from:
- `site/content/`: Hugo documentation site
- `README.md`: Main repository README
- `CONTRIBUTING.md`, `GOVERNANCE.md`, etc.: Repository documentation

When documentation is updated, re-run the indexing:

```bash
python cli.py index --env-file config/.env
```

### Scope

The chatbot is:
- **Domain-restricted**: Only answers Velero-related questions
- **Documentation-focused**: Provides answers based on official docs
- **Non-intrusive**: Separate from main Velero codebase

## Development

### Technology Stack

- **Language**: Python 3.8+
- **AI Service**: Azure OpenAI
- **Vector Databases**: Pinecone, Weaviate
- **CLI Framework**: Click
- **Output Formatting**: Rich

### Code Structure

```
chatbot/src/
├── __init__.py                 # Package initialization
├── config.py                   # Configuration management
├── azure_openai_client.py      # Azure OpenAI integration
├── document_loader.py          # Document processing
├── vector_db.py                # Vector database abstraction
├── rag_system.py               # RAG implementation
└── chatbot.py                  # Main chatbot logic
```

### Dependencies

See [requirements.txt](requirements.txt) for complete list:
- `openai>=1.0.0`: Azure OpenAI SDK
- `pinecone-client>=3.0.0`: Pinecone vector database
- `weaviate-client>=3.25.0`: Weaviate vector database
- `langchain>=0.1.0`: LLM application framework
- `click>=8.1.0`: CLI framework
- `rich>=13.7.0`: Terminal formatting

## Maintenance

### Regular Tasks

- **Documentation Updates**: Re-index when docs change significantly
- **Dependency Updates**: Keep Python packages up to date
- **Configuration**: Rotate API keys periodically

### Cost Considerations

- **Azure OpenAI**:
  - Indexing: ~$0.01-0.05 (one-time per index refresh)
  - Queries: ~$0.001-0.01 per query
  
- **Vector Database**:
  - Pinecone: Free tier available, paid plans from $70/month
  - Weaviate: Free if self-hosted

## Security

- Credentials stored in environment variables
- No hardcoded secrets
- Input validation and sanitization
- Domain restriction (Velero-only queries)

## Testing

Basic validation:

```bash
cd chatbot
python3 validate.py
```

This checks:
- File structure completeness
- Python syntax validity
- Configuration template
- Documentation coverage

## Contributing

The chatbot is designed to be extensible. Possible contributions:

1. **Additional Vector Databases**: Add support for ChromaDB, Qdrant, etc.
2. **Web Interface**: Build a web UI (Flask, FastAPI)
3. **Advanced RAG**: Implement re-ranking, hybrid search
4. **Caching**: Add response caching layer
5. **Analytics**: Track usage and performance

See main [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

## Support

For issues or questions:
- Check [chatbot/README.md](README.md) for troubleshooting
- Review [chatbot/docs/](docs/) for detailed documentation
- Open an issue in the Velero repository
- Ask in [#velero Slack channel](https://kubernetes.slack.com/messages/velero)

## Deployment

The chatbot can be deployed in various ways:

- **Local**: Direct Python execution
- **Docker**: Containerized deployment
- **Kubernetes**: Pod-based deployment
- **Cloud**: Azure Container Instances, AWS ECS, etc.

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment guides.

## Future Enhancements

Potential improvements:

1. Web-based interface
2. Multi-turn conversations with memory
3. Integration with Velero CLI
4. Streaming responses
5. Multi-language support
6. Advanced RAG techniques (hybrid search, re-ranking)

## License

The Velero Chatbot is part of the Velero project and uses the same Apache 2.0 license.

## Acknowledgments

- Built for the [Velero project](https://velero.io/)
- Uses [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- Supports [Pinecone](https://www.pinecone.io/) and [Weaviate](https://weaviate.io/) vector databases
