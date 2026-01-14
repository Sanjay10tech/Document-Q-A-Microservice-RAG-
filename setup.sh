#!/bin/bash

echo "=========================================="
echo "  Document Q&A RAG System - Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null
then
    echo " Python3 not found. Please install Python 3.8+"
    exit 1
fi

echo " Python found:"
python3 --version
echo ""

# Create virtual environment
echo " Creating virtual environment..."
python3 -m venv venv

# Activate venv
echo " Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo " Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt

# Create uploads folder
echo ""
echo "Creating uploads directory..."
mkdir -p uploads

# Create .env file if it doesn't exist
echo ""
echo " Setting up configuration..."
if [ ! -f .env ]; then
    cat > .env << EOF
# Groq API Configuration
# Get your API key from https://console.groq.com
GROQ_API_KEY=your_api_key_here

# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000

# Database Configuration
DATABASE_PATH=documents.db

# Vector Store Configuration
VECTOR_DB_PATH=./chroma_db

# Chunk Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50
EOF
    echo " Created .env file with default configuration"
else
    echo ".env file already exists"
fi

echo ""
echo "=========================================="
echo "   Setup Complete!"
echo "=========================================="
echo ""
echo "Starting the server..."
echo ""

# Run the server
python main.py
