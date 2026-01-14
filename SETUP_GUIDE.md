# Setup Guide for Document Q&A RAG System - Windows

Choose one of the methods below based on your preferred shell:

---

## Method 1: Command Prompt (CMD) - Simplest for Windows

### Step-by-Step:

1. **Open Command Prompt**
   - Press `Win + R`, type `cmd`, press Enter
   - Navigate to project folder:
   ```cmd
   cd C:\Users\DELL\Desktop\document-qa-rag
   ```

2. **Run the batch setup script**
   ```cmd
   setup.bat
   ```
   
3. **Wait for completion**
   - The script will:
     - Check Python installation
     - Create virtual environment
     - Install all dependencies
     - Create `.env` file
     - Start the server automatically
   
4. **Access the application**
   - Once running, open browser to: `http://127.0.0.1:8000`
   - API docs: `http://127.0.0.1:8000/docs`

---

## Method 2: Windows PowerShell - Recommended for Windows Users

### Step-by-Step:

1. **Open Windows PowerShell**
   - Right-click on Start menu → Select "Windows PowerShell" or "Terminal"
   - Navigate to project folder:
   ```powershell
   cd C:\Users\DELL\Desktop\document-qa-rag
   ```

2. **Check PowerShell Execution Policy** (if needed)
   ```powershell
   Get-ExecutionPolicy
   ```

3. **Run the PowerShell setup script**
   
   **Option A: Standard execution**
   ```powershell
   .\setup.ps1
   ```
   
   **Option B: If execution policy error occurs**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then run:
   ```powershell
   .\setup.ps1
   ```
   
   **Option C: Bypass for one-time use**
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup.ps1
   ```

4. **Wait for completion**
   - Script will handle all setup steps automatically

5. **Access the application**
   - Browser: `http://127.0.0.1:8000`
   - Swagger UI: `http://127.0.0.1:8000/docs`

---

## Method 3: Git Bash - For Linux/Unix Users on Windows

### Prerequisites:
- Git for Windows must be installed
- Download from: https://git-scm.com/download/win

### Step-by-Step:

1. **Open Git Bash**
   - Right-click in project folder → "Git Bash Here"
   - OR search "Git Bash" in Windows Start menu

2. **Navigate to project** (if not already there)
   ```bash
   cd /c/Users/DELL/Desktop/document-qa-rag
   ```

3. **Make setup script executable**
   ```bash
   chmod +x setup.sh
   ```

4. **Run the bash setup script**
   ```bash
   ./setup.sh
   ```

5. **Wait for completion**
   - Script will automatically:
     - Create Python virtual environment
     - Install dependencies
     - Create configuration files
     - Start the server

6. **Access the application**
   - Browser: `http://127.0.0.1:8000`
   - API Docs: `http://127.0.0.1:8000/docs`

---

## Method 4: VS Code Terminal (Already Working)

You mentioned this already works! Just continue using it:

```powershell
# In VS Code terminal, run:
.\setup.ps1
```

Or if using Git Bash in VS Code:
```bash
./setup.sh
```

---

## After Setup Completes

### To Stop the Server
- **Command Prompt/PowerShell**: Press `Ctrl + C`
- **Git Bash**: Press `Ctrl + C`

### To Restart the Server Later
1. Open your preferred shell
2. Navigate to project folder
3. **Activate environment** (if not already active)
   - CMD: `venv\Scripts\activate.bat`
   - PowerShell: `.\venv\Scripts\Activate.ps1`
   - Git Bash: `source venv/Scripts/activate`

4. **Start server**
   ```python
   python -m uvicorn main:app --host 127.0.0.1 --port 8000
   ```

---

## Troubleshooting

### Issue: "Python is not installed"
- **Solution**: Install Python 3.13 from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### Issue: "Permission denied" in PowerShell
- **Solution**: Run this once:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Issue: "bash: ./setup.sh: Permission denied" in Git Bash
- **Solution**:
  ```bash
  chmod +x setup.sh
  ./setup.sh
  ```

### Issue: Port 8000 already in use
- **Solution**: Change port in `.env` file and restart

---

## Configuration File (.env)

After first setup, you need to add your **Groq API Key**:

1. Open `.env` file in editor
2. Replace `your_groq_api_key_here` with your actual key
3. Save the file
4. Restart the server

---

## Recommended Method

**For Windows Users**: Use **Method 1 (Command Prompt)** or **Method 2 (PowerShell)**
- Simplest setup
- No additional software needed
- Fastest execution

**For Linux/Mac Users on Windows**: Use **Method 3 (Git Bash)**
- Familiar shell environment
- Same commands as Linux/Mac
