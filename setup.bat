@echo off
REM Document Q&A RAG System - Windows Setup Script

echo.
echo ==========================================
echo   Document Q&A RAG System - Setup
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo FAILED: Python not found. Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Found Python:
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies
echo.
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt

REM Create uploads folder
echo.
echo Creating uploads directory...
if not exist "uploads" mkdir uploads

REM Create .env file if it doesn't exist
echo.
echo Setting up configuration...
if not exist ".env" (
    (
        echo # Groq API Configuration
        echo # Get your API key from https://console.groq.com
        echo GROQ_API_KEY=your_groq_api_key_here
        echo.
        echo # Server Configuration
        echo SERVER_HOST=127.0.0.1
        echo SERVER_PORT=8000
        echo.
        echo # Database Configuration
        echo DATABASE_PATH=documents.db
        echo.
        echo # Vector Store Configuration
        echo VECTOR_DB_PATH=./chroma_db
        echo.
        echo # Chunk Configuration
        echo CHUNK_SIZE=500
        echo CHUNK_OVERLAP=50
    ) > .env
    echo Created .env file with default configuration
) else (
    echo .env file already exists
)

echo.
echo ==========================================
echo   Setup Complete!
echo ==========================================
echo.
echo Starting the server...
echo.
echo Open your browser at: http://127.0.0.1:8000/docs
echo.

REM Run the server
python main.py

pause
