@echo off
REM ============================================
REM Health AI - One-Click Start Script
REM ============================================

echo.
echo ╔════════════════════════════════════════╗
echo ║  🏥 Health AI System - Starting...     ║
echo ╚════════════════════════════════════════╝
echo.

REM Check if running as admin (optional)
setlocal enabledelayedexpansion

REM Get current directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Terminal 1: Start Backend
echo [1/2] Starting Backend Server...
start cmd /k "cd backend && python app.py"

REM Wait for backend to start
echo [⏳] Waiting for backend to initialize...
timeout /t 3 /nobreak

REM Terminal 2: Start Frontend
echo [2/2] Starting Frontend...
start cmd /k "cd frontend && npm start"

echo.
echo ╔════════════════════════════════════════╗
echo ║  ✅ Both services are starting!       ║
echo ╠════════════════════════════════════════╣
echo ║  Backend:  http://localhost:5000      ║
echo ║  Frontend: http://localhost:3000      ║
echo ║                                        ║
echo ║  ⏳ Wait 10-15 seconds for npm...     ║
echo ║  🌐 Browser will open automatically   ║
echo ╚════════════════════════════════════════╝
echo.

REM Give user time to read the message
timeout /t 5 /nobreak

REM Try to open browser
echo Opening browser...
start http://localhost:3000

echo.
echo 💡 Tips:
echo   - Check backend terminal for model loading messages
echo   - Check frontend terminal for npm status
echo   - If browser doesn't open, visit http://localhost:3000 manually
echo   - Close either terminal window to stop that service
echo.

REM Keep this window open
pause
