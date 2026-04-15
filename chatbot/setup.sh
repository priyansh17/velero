#!/bin/bash

# Velero Chatbot Setup Script
# This script helps you set up the Velero Chatbot quickly

set -e

echo "========================================="
echo "Velero Chatbot Setup Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python $REQUIRED_VERSION or higher is required${NC}"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

echo -e "${GREEN}✓ Python version is compatible${NC}"
echo ""

# Ask about virtual environment
echo "Would you like to create a virtual environment? (recommended)"
read -p "Create venv? [Y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment created and activated${NC}"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}Error: Failed to install dependencies${NC}"
    exit 1
fi
echo ""

# Create config directory if it doesn't exist
mkdir -p config

# Check if .env exists
if [ -f "config/.env" ]; then
    echo -e "${YELLOW}Warning: config/.env already exists${NC}"
    read -p "Overwrite? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp config/.env.example config/.env
        echo -e "${GREEN}✓ Configuration file created${NC}"
    else
        echo "Keeping existing configuration"
    fi
else
    cp config/.env.example config/.env
    echo -e "${GREEN}✓ Configuration file created${NC}"
fi
echo ""

# Interactive configuration
echo "========================================="
echo "Azure OpenAI Configuration"
echo "========================================="
echo ""
echo "You need to configure Azure OpenAI credentials."
echo "Get these from: https://portal.azure.com"
echo ""

read -p "Enter Azure OpenAI API Key: " AZURE_KEY
read -p "Enter Azure OpenAI Endpoint: " AZURE_ENDPOINT
read -p "Enter Chat Deployment Name: " DEPLOYMENT_NAME
read -p "Enter Embedding Deployment Name: " EMBEDDING_NAME

# Update .env file
sed -i.bak "s|AZURE_OPENAI_API_KEY=.*|AZURE_OPENAI_API_KEY=$AZURE_KEY|" config/.env
sed -i.bak "s|AZURE_OPENAI_ENDPOINT=.*|AZURE_OPENAI_ENDPOINT=$AZURE_ENDPOINT|" config/.env
sed -i.bak "s|AZURE_OPENAI_DEPLOYMENT_NAME=.*|AZURE_OPENAI_DEPLOYMENT_NAME=$DEPLOYMENT_NAME|" config/.env
sed -i.bak "s|AZURE_OPENAI_EMBEDDING_DEPLOYMENT=.*|AZURE_OPENAI_EMBEDDING_DEPLOYMENT=$EMBEDDING_NAME|" config/.env
rm -f config/.env.bak

echo ""
echo "========================================="
echo "RAG Configuration"
echo "========================================="
echo ""
echo "Do you want to enable RAG (Retrieval-Augmented Generation)?"
echo "RAG provides better, context-aware answers but requires a vector database."
echo ""
read -p "Enable RAG? [Y/n] " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    echo ""
    echo "Select Vector Database:"
    echo "1) Pinecone (cloud-based, free tier available)"
    echo "2) Weaviate (can run locally with Docker)"
    read -p "Choice [1-2]: " -n 1 -r DB_CHOICE
    echo ""
    
    if [[ $DB_CHOICE == "1" ]]; then
        echo ""
        read -p "Enter Pinecone API Key: " PINECONE_KEY
        read -p "Enter Pinecone Environment (e.g., us-east-1-aws): " PINECONE_ENV
        
        sed -i.bak "s|PINECONE_API_KEY=.*|PINECONE_API_KEY=$PINECONE_KEY|" config/.env
        sed -i.bak "s|PINECONE_ENVIRONMENT=.*|PINECONE_ENVIRONMENT=$PINECONE_ENV|" config/.env
        sed -i.bak "s|VECTOR_DB_TYPE=.*|VECTOR_DB_TYPE=pinecone|" config/.env
        sed -i.bak "s|ENABLE_RAG=.*|ENABLE_RAG=true|" config/.env
        rm -f config/.env.bak
        
        echo -e "${GREEN}✓ Pinecone configured${NC}"
    elif [[ $DB_CHOICE == "2" ]]; then
        echo ""
        read -p "Enter Weaviate URL (default: http://localhost:8080): " WEAVIATE_URL
        WEAVIATE_URL=${WEAVIATE_URL:-http://localhost:8080}
        
        sed -i.bak "s|WEAVIATE_URL=.*|WEAVIATE_URL=$WEAVIATE_URL|" config/.env
        sed -i.bak "s|VECTOR_DB_TYPE=.*|VECTOR_DB_TYPE=weaviate|" config/.env
        sed -i.bak "s|ENABLE_RAG=.*|ENABLE_RAG=true|" config/.env
        rm -f config/.env.bak
        
        echo -e "${GREEN}✓ Weaviate configured${NC}"
        
        # Check if Docker is available
        if command -v docker &> /dev/null; then
            echo ""
            read -p "Start local Weaviate with Docker? [Y/n] " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
                docker run -d -p 8080:8080 --name weaviate semitechnologies/weaviate:latest
                echo -e "${GREEN}✓ Weaviate started on http://localhost:8080${NC}"
            fi
        fi
    fi
else
    sed -i.bak "s|ENABLE_RAG=.*|ENABLE_RAG=false|" config/.env
    rm -f config/.env.bak
    echo -e "${YELLOW}RAG disabled - using direct query mode${NC}"
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""

# Check if RAG is enabled
if grep -q "ENABLE_RAG=true" config/.env; then
    echo "Next steps:"
    echo ""
    echo "1. Index the repository (required for RAG):"
    echo "   python cli.py index --env-file config/.env"
    echo ""
    echo "2. Start chatting:"
    echo "   python cli.py chat --env-file config/.env"
    echo ""
    echo "3. Check status:"
    echo "   python cli.py status --env-file config/.env"
else
    echo "Next steps:"
    echo ""
    echo "1. Start chatting:"
    echo "   python cli.py chat --env-file config/.env"
    echo ""
    echo "2. Check status:"
    echo "   python cli.py status --env-file config/.env"
fi

echo ""
echo "For more information, see:"
echo "  - README.md"
echo "  - docs/QUICKSTART.md"
echo "  - docs/CONFIGURATION.md"
echo ""

if [ -f "venv/bin/activate" ]; then
    echo -e "${YELLOW}Note: Virtual environment is activated.${NC}"
    echo "To activate it later, run: source venv/bin/activate"
fi
