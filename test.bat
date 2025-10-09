@echo off
chcp 65001 > nul
echo ========================================
echo FBC Creators Local Server
echo ========================================
echo.

cd /d "C:\Users\movemin\Desktop\새 폴더\FBC"

REM Check folder structure
echo [1/3] Checking folder structure...
if not exist "data" (
    echo   [ERROR] 'data' folder not found!
    echo   Creating 'data' folder...
    mkdir data
    echo   [OK] Created 'data' folder
) else (
    echo   [OK] 'data' folder exists
)
echo.

REM Check JSON files
echo [2/3] Checking required JSON files...
set "missing=0"

if not exist "data\hero.json" (
    echo   [MISSING] data\hero.json
    set "missing=1"
) else (
    echo   [OK] data\hero.json
)

if not exist "data\headlines.json" (
    echo   [MISSING] data\headlines.json
    set "missing=1"
) else (
    echo   [OK] data\headlines.json
)

if not exist "data\fashion.json" (
    echo   [MISSING] data\fashion.json
    set "missing=1"
) else (
    echo   [OK] data\fashion.json
)

if not exist "data\beauty.json" (
    echo   [MISSING] data\beauty.json
    set "missing=1"
) else (
    echo   [OK] data\beauty.json
)

if not exist "data\life.json" (
    echo   [MISSING] data\life.json
    set "missing=1"
) else (
    echo   [OK] data\life.json
)

if not exist "data\districts.json" (
    echo   [MISSING] data\districts.json
    set "missing=1"
) else (
    echo   [OK] data\districts.json
)

if not exist "data\areas.json" (
    echo   [MISSING] data\areas.json
    set "missing=1"
) else (
    echo   [OK] data\areas.json
)

echo.

if "%missing%"=="1" (
    echo ========================================
    echo [WARNING] Some JSON files are missing!
    echo ========================================
    echo.
    echo The website may not work properly.
    echo Please make sure all JSON files are in the 'data' folder.
    echo.
    echo Do you want to continue anyway? (Y/N)
    set /p "continue=Your choice: "
    
    if /i not "%continue%"=="Y" (
        echo.
        echo Server startup cancelled.
        pause
        exit /b
    )
    echo.
)

REM Find IP address
echo [3/3] Getting network information...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr /v "127.0.0.1"') do (
    set IP=%%a
    goto :found
)
:found
set IP=%IP: =%

echo.
echo ========================================
echo Server is starting...
echo ========================================
echo.
echo   Local:   http://localhost:8000
echo   Network: http://%IP%:8000
echo.
echo Opening browser...
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Open browser
start http://localhost:8000

REM Start server
python -m http.server 8000

pause
