# Velero Chatbot - Usage Examples and Screenshots

This document shows examples of how to use the Velero Chatbot and what the interactions look like.

## Installation and Setup

### Quick Setup

```bash
cd velero/chatbot
./setup.sh
```

The setup script will guide you through:
1. Checking Python version
2. Creating virtual environment
3. Installing dependencies
4. Configuring Azure OpenAI
5. Setting up vector database (optional)

## Command Line Interface

### Available Commands

The chatbot provides three main commands:

```bash
# Index repository documents (required for RAG mode)
python cli.py index --env-file config/.env

# Interactive chat mode
python cli.py chat --env-file config/.env

# Single query mode
python cli.py chat --env-file config/.env --query "What is Velero?"

# Check system status
python cli.py status --env-file config/.env
```

## Example Sessions

### Example 1: First Time Setup

```
$ python cli.py status --env-file config/.env

╭─────────── Velero Chatbot Status ───────────╮
│                                              │
│ RAG Mode: ✓ Enabled                         │
│ Vector Database Type: pinecone              │
│ Index Ready: ✗ No                           │
│ Azure OpenAI: ✓ Configured                  │
│                                              │
╰──────────────────────────────────────────────╯

⚠ Vector database index not found. Run 'index' command first.
```

### Example 2: Indexing Documents

```
$ python cli.py index --env-file config/.env

Velero Chatbot - Repository Indexing

Initializing chatbot...
Starting repository indexing...
Repository path: ../
Documentation path: ../site/content
Vector DB: pinecone

Preparing documents for indexing...
Loading documents...
Loading documentation files: 100%|██████████| 45/45 [00:02<00:00, 18.23 files/s]
Loaded 50 documents

Chunking documents...
Chunking documents: 100%|██████████| 50/50 [00:01<00:00, 42.33 docs/s]
Created 287 chunks

Generating embeddings for 287 chunks...
Generated embeddings for 50/287 chunks
Generated embeddings for 100/287 chunks
Generated embeddings for 150/287 chunks
Generated embeddings for 200/287 chunks
Generated embeddings for 250/287 chunks
Generated embeddings for 287/287 chunks

Creating/verifying vector database index...
Created index velero-docs

Indexing documents in vector database...
Indexed 287 documents

✓ Repository indexing completed successfully!
```

### Example 3: Interactive Chat Session

```
$ python cli.py chat --env-file config/.env

Velero Chatbot
Initializing...

╭─────────── Chatbot Status ───────────╮
│                                       │
│ RAG Mode: Enabled                     │
│ Vector DB: pinecone                   │
│ Index Ready: Yes                      │
│                                       │
╰───────────────────────────────────────╯

Type your questions about Velero. Type 'exit' or 'quit' to end the session.


You: What is Velero?

Thinking...

Assistant
╭────────────────── Answer (RAG) ──────────────────╮
│                                                   │
│ Velero (formerly Heptio Ark) is an open source   │
│ tool that gives you the ability to back up and    │
│ restore your Kubernetes cluster resources and     │
│ persistent volumes. It can be run with a public   │
│ cloud platform or on-premises.                    │
│                                                   │
│ Key capabilities of Velero include:               │
│                                                   │
│ • **Backup**: Take backups of your cluster and    │
│   restore in case of loss                         │
│ • **Migration**: Migrate cluster resources to     │
│   other clusters                                  │
│ • **Replication**: Replicate your production      │
│   cluster to development and testing clusters     │
│                                                   │
│ Velero consists of two main components:           │
│ 1. A server that runs on your cluster             │
│ 2. A command-line client that runs locally        │
│                                                   │
╰───────────────────────────────────────────────────╯

╭──────────────────── Sources ─────────────────────╮
│                                                   │
│ • README.md (relevance: 0.92)                     │
│ • site/content/docs/main/index.md (relevance: 0.88) │
│ • site/content/_index.md (relevance: 0.85)        │
│                                                   │
╰───────────────────────────────────────────────────╯


You: How do I create a backup?

Thinking...

Assistant
╭────────────────── Answer (RAG) ──────────────────╮
│                                                   │
│ To create a backup with Velero, use the          │
│ `velero backup create` command:                   │
│                                                   │
│ **Basic Backup:**                                 │
│ ```bash                                           │
│ velero backup create my-backup                    │
│ ```                                               │
│                                                   │
│ **Backup Specific Namespace:**                    │
│ ```bash                                           │
│ velero backup create my-backup \                  │
│   --include-namespaces=my-namespace               │
│ ```                                               │
│                                                   │
│ **Backup with Specific Resources:**               │
│ ```bash                                           │
│ velero backup create my-backup \                  │
│   --include-resources=pods,services               │
│ ```                                               │
│                                                   │
│ **Scheduled Backup:**                             │
│ ```bash                                           │
│ velero schedule create daily-backup \             │
│   --schedule="0 2 * * *"                          │
│ ```                                               │
│                                                   │
│ You can check backup status with:                │
│ ```bash                                           │
│ velero backup describe my-backup                  │
│ velero backup logs my-backup                      │
│ ```                                               │
│                                                   │
╰───────────────────────────────────────────────────╯

╭──────────────────── Sources ─────────────────────╮
│                                                   │
│ • site/content/docs/main/backup.md (0.94)         │
│ • site/content/docs/main/cli.md (0.87)            │
│ • examples/backup-example.yaml (0.82)             │
│                                                   │
╰───────────────────────────────────────────────────╯


You: exit

Goodbye! 👋
```

### Example 4: Single Query Mode

```
$ python cli.py chat --env-file config/.env \
  --query "What cloud providers does Velero support?"

Velero Chatbot
Initializing...

╭─────────── Chatbot Status ───────────╮
│                                       │
│ RAG Mode: Enabled                     │
│ Vector DB: pinecone                   │
│ Index Ready: Yes                      │
│                                       │
╰───────────────────────────────────────╯

Thinking...

Assistant
╭────────────────── Answer (RAG) ──────────────────╮
│                                                   │
│ Velero supports the following cloud providers:    │
│                                                   │
│ • **AWS (Amazon Web Services)**                   │
│   - S3 for backup storage                         │
│   - EBS snapshots for persistent volumes          │
│                                                   │
│ • **Azure (Microsoft Azure)**                     │
│   - Azure Blob Storage for backups                │
│   - Azure Disk snapshots                          │
│                                                   │
│ • **GCP (Google Cloud Platform)**                 │
│   - Google Cloud Storage for backups              │
│   - Persistent disk snapshots                     │
│                                                   │
│ • **On-Premises and Other Cloud Providers**       │
│   - Any S3-compatible storage (MinIO, etc.)       │
│   - Restic for file-level backups                 │
│   - CSI snapshots for any CSI-compatible storage  │
│                                                   │
│ Velero also supports hybrid and multi-cloud       │
│ scenarios, allowing you to back up from one       │
│ provider and restore to another.                  │
│                                                   │
╰───────────────────────────────────────────────────╯

╭──────────────────── Sources ─────────────────────╮
│                                                   │
│ • site/content/docs/main/supported-providers.md   │
│   (relevance: 0.95)                               │
│ • README.md (relevance: 0.88)                     │
│ • site/content/docs/main/install.md (0.84)        │
│                                                   │
╰───────────────────────────────────────────────────╯
```

### Example 5: Direct Mode (No RAG)

When RAG is disabled (`ENABLE_RAG=false`):

```
$ python cli.py chat --env-file config/.env

Velero Chatbot
Initializing...

╭─────────── Chatbot Status ───────────╮
│                                       │
│ RAG Mode: Disabled                    │
│ Vector DB: N/A                        │
│ Index Ready: N/A                      │
│                                       │
╰───────────────────────────────────────╯


You: What is Velero?

Thinking...

Assistant
╭───────────────── Answer (DIRECT) ────────────────╮
│                                                   │
│ Velero is an open source tool for backing up and  │
│ restoring Kubernetes cluster resources and        │
│ persistent volumes. It was formerly known as      │
│ Heptio Ark. Velero helps you:                     │
│                                                   │
│ 1. Back up your Kubernetes cluster resources      │
│ 2. Restore your cluster in case of loss           │
│ 3. Migrate cluster resources to other clusters    │
│ 4. Replicate production environments to dev/test  │
│                                                   │
│ Velero runs as a deployment in your Kubernetes    │
│ cluster and provides a CLI for management.        │
│                                                   │
╰───────────────────────────────────────────────────╯
```

Note: Direct mode doesn't show sources since it doesn't retrieve from documentation.

## Status Checking

### Healthy System

```
$ python cli.py status --env-file config/.env

Velero Chatbot Status

╭──────────── Status Information ─────────────╮
│                                              │
│ RAG Mode: ✓ Enabled                         │
│ Vector Database Type: pinecone              │
│ Index Ready: ✓ Yes                          │
│ Azure OpenAI: ✓ Configured                  │
│                                              │
╰──────────────────────────────────────────────╯
```

### Missing Configuration

```
$ python cli.py status --env-file config/.env

Error: AZURE_OPENAI_API_KEY is required
```

### Missing Index

```
$ python cli.py status --env-file config/.env

Velero Chatbot Status

╭──────────── Status Information ─────────────╮
│                                              │
│ RAG Mode: ✓ Enabled                         │
│ Vector Database Type: pinecone              │
│ Index Ready: ✗ No                           │
│ Azure OpenAI: ✓ Configured                  │
│                                              │
╰──────────────────────────────────────────────╯

⚠ Vector database index not found. Run 'index' command first.
```

## Common Usage Patterns

### Learning About Velero

```
You: What is Velero?
You: How does Velero differ from other backup solutions?
You: What are the main components of Velero?
```

### Installation and Setup

```
You: How do I install Velero on AWS?
You: What are the prerequisites for Velero?
You: How do I configure backup storage?
```

### Operations

```
You: How do I create a backup?
You: How can I schedule automatic backups?
You: What's the process for restoring a backup?
You: How do I restore to a different namespace?
```

### Troubleshooting

```
You: Why is my backup failing?
You: How do I debug Velero issues?
You: Where can I find Velero logs?
You: My backup is stuck in progress state, what should I check?
```

### Advanced Topics

```
You: How does Velero handle persistent volume snapshots?
You: What's the difference between Restic and CSI snapshots?
You: How do I configure backup hooks?
You: Can I migrate between different cloud providers?
```

## Features Demonstrated

### 1. Rich Formatting
- Color-coded output
- Markdown rendering in answers
- Boxed panels for better readability
- Progress bars during indexing

### 2. Source Attribution
- Shows which documents were used
- Relevance scores for each source
- Helps verify answer accuracy

### 3. Context Awareness (RAG Mode)
- Retrieves relevant documentation
- Provides detailed, accurate answers
- Cites specific documentation sections

### 4. User-Friendly Interaction
- Natural language queries
- Interactive mode with history
- Single query mode for scripts
- Status checking for diagnostics

### 5. Flexible Configuration
- RAG mode for accuracy
- Direct mode for quick setup
- Multiple vector database options
- Tunable parameters

## Tips for Best Results

1. **Be Specific**: "How do I backup a namespace called 'production'?" vs "How do I backup?"

2. **Use RAG Mode**: Enables source attribution and more accurate answers

3. **Keep Index Updated**: Re-run `index` command when documentation changes

4. **Check Status**: Use `status` command to verify configuration

5. **Review Sources**: Check cited sources to verify answer accuracy

## Next Steps

- Try the example queries in `examples/example_queries.md`
- Configure your own Azure OpenAI credentials
- Index your repository documentation
- Start chatting with the bot!

For more information:
- See [README.md](README.md) for complete documentation
- Check [docs/QUICKSTART.md](docs/QUICKSTART.md) for 5-minute setup
- Review [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for advanced options
