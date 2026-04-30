# Deployment Guide

This guide covers deploying the Velero Chatbot in various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

## Local Development

### Quick Setup

1. **Clone and navigate**:
   ```bash
   cd velero/chatbot
   ```

2. **Run setup script**:
   ```bash
   ./setup.sh
   ```
   
   This interactive script will:
   - Check Python version
   - Create virtual environment
   - Install dependencies
   - Configure Azure OpenAI
   - Set up vector database (optional)

3. **Activate environment**:
   ```bash
   source venv/bin/activate
   ```

4. **Index (if using RAG)**:
   ```bash
   python cli.py index --env-file config/.env
   ```

5. **Start chatting**:
   ```bash
   python cli.py chat --env-file config/.env
   ```

### Manual Setup

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp config/.env.example config/.env
# Edit config/.env with your credentials

# Index (for RAG)
python cli.py index --env-file config/.env

# Run
python cli.py chat --env-file config/.env
```

## Docker Deployment

### Build Docker Image

Create `Dockerfile` in the chatbot directory:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directory for config
RUN mkdir -p /app/config

# Set environment variables (optional defaults)
ENV PYTHONUNBUFFERED=1

# Run chatbot
ENTRYPOINT ["python", "cli.py"]
CMD ["chat"]
```

Build:

```bash
docker build -t velero-chatbot:latest .
```

### Run with Docker

**Interactive mode**:

```bash
docker run -it \
  --env-file config/.env \
  velero-chatbot:latest chat
```

**Single query**:

```bash
docker run \
  --env-file config/.env \
  velero-chatbot:latest chat \
  --query "What is Velero?"
```

**Indexing**:

```bash
docker run \
  --env-file config/.env \
  velero-chatbot:latest index
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # Optional: Local Weaviate instance
  weaviate:
    image: semitechnologies/weaviate:latest
    ports:
      - "8080:8080"
    environment:
      - AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true
      - PERSISTENCE_DATA_PATH=/var/lib/weaviate

  chatbot:
    build: .
    env_file:
      - config/.env
    depends_on:
      - weaviate
    stdin_open: true
    tty: true
    command: chat
```

Run:

```bash
# Start services
docker-compose up -d weaviate

# Index documents
docker-compose run chatbot index

# Start chatbot
docker-compose run chatbot chat
```

## Cloud Deployment

### Azure Container Instances

1. **Create Azure Container Registry**:
   ```bash
   az acr create --resource-group myResourceGroup \
     --name veleroregistry --sku Basic
   ```

2. **Build and push image**:
   ```bash
   az acr build --registry veleroregistry \
     --image velero-chatbot:latest .
   ```

3. **Deploy**:
   ```bash
   az container create \
     --resource-group myResourceGroup \
     --name velero-chatbot \
     --image veleroregistry.azurecr.io/velero-chatbot:latest \
     --environment-variables \
       AZURE_OPENAI_API_KEY=$AZURE_KEY \
       AZURE_OPENAI_ENDPOINT=$AZURE_ENDPOINT \
       PINECONE_API_KEY=$PINECONE_KEY \
     --interactive
   ```

### AWS ECS

1. **Create ECR repository**:
   ```bash
   aws ecr create-repository --repository-name velero-chatbot
   ```

2. **Build and push**:
   ```bash
   docker tag velero-chatbot:latest \
     $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/velero-chatbot:latest
   
   docker push $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/velero-chatbot:latest
   ```

3. **Create ECS task definition** and service.

### Kubernetes Deployment

Create `k8s-deployment.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: chatbot-secrets
type: Opaque
stringData:
  azure-openai-key: "your-key"
  pinecone-key: "your-key"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: velero-chatbot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: velero-chatbot
  template:
    metadata:
      labels:
        app: velero-chatbot
    spec:
      containers:
      - name: chatbot
        image: velero-chatbot:latest
        env:
        - name: AZURE_OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: chatbot-secrets
              key: azure-openai-key
        - name: AZURE_OPENAI_ENDPOINT
          value: "https://your-resource.openai.azure.com/"
        - name: AZURE_OPENAI_DEPLOYMENT_NAME
          value: "gpt-35-turbo"
        - name: PINECONE_API_KEY
          valueFrom:
            secretKeyRef:
              name: chatbot-secrets
              key: pinecone-key
        - name: ENABLE_RAG
          value: "true"
        stdin: true
        tty: true
```

Deploy:

```bash
kubectl apply -f k8s-deployment.yaml
```

## Production Considerations

### 1. Security

**Secrets Management**:
- Use Azure Key Vault, AWS Secrets Manager, or HashiCorp Vault
- Never commit secrets to version control
- Rotate keys regularly

**Example with Azure Key Vault**:
```bash
# Store secrets
az keyvault secret set \
  --vault-name myKeyVault \
  --name azure-openai-key \
  --value "your-key"

# Retrieve in code
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://mykeyvault.vault.azure.net/", credential=credential)
secret = client.get_secret("azure-openai-key")
```

**Network Security**:
- Use private endpoints for Azure OpenAI
- VPN or VNet integration
- Firewall rules for vector databases

### 2. Monitoring and Logging

**Logging Configuration**:

Create `logging_config.py`:

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
        }
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('chatbot.log')
    ]
)
logger = logging.getLogger(__name__)
```

**Metrics to Track**:
- Query latency
- Success/failure rate
- Token usage
- Cost per query
- Vector DB performance

**Tools**:
- Azure Monitor / Application Insights
- AWS CloudWatch
- Prometheus + Grafana

### 3. High Availability

**Load Balancing**:
- Multiple chatbot instances behind load balancer
- Health check endpoint

**Failover**:
- Multiple Azure OpenAI deployments
- Fallback vector databases
- Circuit breaker pattern

### 4. Cost Optimization

**Azure OpenAI**:
- Use GPT-3.5-turbo for cost-effective responses
- Implement caching for common queries
- Set token limits

**Vector Database**:
- Use appropriate tier (Pinecone free tier for dev)
- Clean up old indexes
- Optimize chunk size

**Caching Strategy**:

```python
from functools import lru_cache
import hashlib

class CachedChatbot:
    def __init__(self, chatbot):
        self.chatbot = chatbot
        self.cache = {}
    
    def query(self, question):
        cache_key = hashlib.md5(question.encode()).hexdigest()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = self.chatbot.query(question)
        self.cache[cache_key] = result
        return result
```

### 5. Rate Limiting

Implement rate limiting to prevent abuse:

```python
from time import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def allow_request(self, user_id):
        now = time()
        user_requests = self.requests[user_id]
        
        # Remove old requests
        user_requests[:] = [t for t in user_requests if now - t < self.window_seconds]
        
        if len(user_requests) >= self.max_requests:
            return False
        
        user_requests.append(now)
        return True
```

### 6. Web API Deployment

Create REST API for web integration:

**`api.py`**:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.config import Config
from src.chatbot import VeleroChatbot

app = Flask(__name__)
CORS(app)

config = Config()
chatbot = VeleroChatbot(config)

@app.route('/api/health', methods=['GET'])
def health():
    status = chatbot.get_status()
    return jsonify({'status': 'healthy', 'details': status})

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'Question required'}), 400
    
    result = chatbot.query(question)
    return jsonify(result)

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify(chatbot.get_status())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

**Deploy with Gunicorn**:

```bash
pip install gunicorn flask flask-cors
gunicorn -w 4 -b 0.0.0.0:8000 api:app
```

**Nginx Configuration**:

```nginx
server {
    listen 80;
    server_name chatbot.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 7. Continuous Deployment

**GitHub Actions** (`.github/workflows/deploy.yml`):

```yaml
name: Deploy Chatbot

on:
  push:
    branches: [main]
    paths:
      - 'chatbot/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: |
          cd chatbot
          docker build -t velero-chatbot:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          echo ${{ secrets.REGISTRY_PASSWORD }} | docker login -u ${{ secrets.REGISTRY_USERNAME }} --password-stdin
          docker push velero-chatbot:${{ github.sha }}
      
      - name: Deploy
        run: |
          # Deployment commands
```

### 8. Backup and Recovery

**Vector Database Backup**:

Pinecone:
```python
# Export index
from pinecone import Pinecone
pc = Pinecone(api_key="key")
index = pc.Index("velero-docs")

# Use describe_index_stats() to monitor
stats = index.describe_index_stats()
```

Weaviate:
```bash
# Backup using Weaviate backup API
curl -X POST "http://localhost:8080/v1/backups"
```

**Configuration Backup**:
- Version control for code
- Secure backup of `.env` files
- Document manual configuration steps

## Troubleshooting Production Issues

### High Latency

1. Check Azure OpenAI region (use nearest)
2. Reduce `TOP_K_RESULTS`
3. Implement caching
4. Use faster vector DB tier

### High Costs

1. Monitor token usage
2. Implement query caching
3. Use GPT-3.5 instead of GPT-4
4. Set lower `MAX_TOKENS`

### Connection Failures

1. Check API keys and endpoints
2. Verify network connectivity
3. Check rate limits
4. Review logs for errors

### Poor Answer Quality

1. Re-index with better chunking
2. Increase `TOP_K_RESULTS`
3. Improve system prompts
4. Use GPT-4 for better reasoning

## Support and Maintenance

### Regular Tasks

- **Weekly**: Monitor costs and usage
- **Monthly**: Review logs and errors
- **Quarterly**: Re-index documentation
- **Yearly**: Rotate API keys

### Updates

- Keep dependencies updated
- Monitor for security vulnerabilities
- Update models as new versions release

### Documentation

- Maintain deployment runbooks
- Document configuration changes
- Keep architecture diagrams updated
