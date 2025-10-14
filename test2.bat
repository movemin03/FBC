@echo off
chcp 65001 > nul
echo ========================================
echo FBC Creators Local Server
echo ========================================
echo.

REM Get the directory where the batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if index.html exists
echo [1/4] Checking index.html...
if not exist "index.html" (
    echo   [ERROR] index.html not found in current directory!
    echo   Current directory: %SCRIPT_DIR%
    echo.
    pause
    exit /b
) else (
    echo   [OK] index.html found
)
echo.

REM Check folder structure
echo [2/4] Checking folder structure...
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
echo [3/4] Checking required JSON files...
set "missing=0"

if not exist "data\pinned.json" (
    echo   [MISSING] data\pinned.json
    set "missing=1"
) else (
    echo   [OK] data\pinned.json
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

if not exist "data\district_meta.json" (
    echo   [MISSING] data\district_meta.json
    set "missing=1"
) else (
    echo   [OK] data\district_meta.json
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
    echo Required files:
    echo   - pinned.json
    echo   - fashion.json
    echo   - beauty.json
    echo   - life.json
    echo   - districts.json
    echo   - district_meta.json
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
echo [4/4] Getting network information...
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
echo   Location: %SCRIPT_DIR%
echo   Local:    http://localhost:8000
echo   Network:  http://%IP%:8000
echo.
echo Opening browser...
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Open browser (index.html in current directory)
start http://localhost:8000/article/index.html?category=fashion&id=fs00006

REM Start server
python -m http.server 8000

pause
