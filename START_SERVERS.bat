@echo off
echo ========================================
echo   VASTU VISION - STARTING SERVERS
echo ========================================
echo.

echo [1/2] Starting Python HTTP Server (Port 8000)...
start "HTTP Server" cmd /k "python -m http.server 8000"
timeout /t 2 /nobreak >nul

echo [2/2] Starting ML Analysis Server (Port 5000)...
start "ML Server" cmd /k "python analyze_vastu.py"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   SERVERS RUNNING!
echo ========================================
echo.
echo Frontend: http://localhost:8000
echo ML Backend: http://localhost:5000
echo.
echo OPEN THIS URL:
echo http://localhost:8000/DEMO_INDEX.html
echo.
echo Press any key to open in browser...
pause >nul

start http://localhost:8000/DEMO_INDEX.html

echo.
echo Servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause

