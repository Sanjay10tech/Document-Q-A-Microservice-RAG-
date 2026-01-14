# Document Q&A RAG System Setup Script for PowerShell
# This script sets up the entire project on Windows

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Document Q&A RAG System Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.13+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonCheck" -ForegroundColor Green
Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Virtual environment created successfully" -ForegroundColor Green
    } else {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -eq 0) {
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host ""

# Install requirements
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "requirements.txt not found" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env configuration file..." -ForegroundColor Yellow
    $envContent = @"
GROQ_API_KEY=your_groq_api_key_here
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
DATABASE_PATH=documents.db
VECTOR_DB_PATH=./chroma_db
CHUNK_SIZE=500
CHUNK_OVERLAP=50
"@
    Set-Content -Path ".env" -Value $envContent
    Write-Host ".env file created with default values" -ForegroundColor Green
    Write-Host "Please update .env with your GROQ_API_KEY" -ForegroundColor Yellow
} else {
    Write-Host ".env file already exists" -ForegroundColor Green
}
Write-Host ""

# Start the server
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Starting RAG System Server..." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server will be available at: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "API documentation: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn main:app --host 127.0.0.1 --port 8000
