# Physical AI Textbook - Development Startup Script (PowerShell)
# Run this script to start both frontend and backend in separate windows

Write-Host "🚀 Starting Physical AI Textbook Development Environment" -ForegroundColor Cyan
Write-Host "=" -repeat 60 -ForegroundColor Gray

# Check if backend .env exists
if (-not (Test-Path "backend\.env")) {
    Write-Host "⚠️  Warning: backend\.env not found!" -ForegroundColor Yellow
    Write-Host "📝 Please create backend\.env with your API keys" -ForegroundColor Yellow
    Write-Host "   See backend\.env.example for template" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit
    }
}

# Check if node_modules exists in frontend
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
    Push-Location frontend
    npm install
    Pop-Location
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
}

# Check if Python venv exists in backend
if (-not (Test-Path "backend\venv")) {
    Write-Host "🐍 Creating Python virtual environment..." -ForegroundColor Yellow
    Push-Location backend
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    deactivate
    Pop-Location
    Write-Host "✅ Backend dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🔧 Starting services in new windows..." -ForegroundColor Cyan

# Start backend in new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\venv\Scripts\Activate.ps1; Write-Host '🔥 Backend Server Starting...' -ForegroundColor Green; python main.py"

# Wait a moment for backend to initialize
Start-Sleep -Seconds 3

# Start frontend in new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; Write-Host '⚡ Frontend Server Starting...' -ForegroundColor Green; npm start"

Write-Host ""
Write-Host "✅ Services started in separate windows!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Wait for both servers to start (~30 seconds)" -ForegroundColor White
Write-Host "  2. Run ingestion (if first time):" -ForegroundColor White
Write-Host "     cd backend && python ingest_textbook.py" -ForegroundColor Gray
Write-Host "  3. Open http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop: Close the PowerShell windows or press Ctrl+C in each" -ForegroundColor Yellow
Write-Host ""
