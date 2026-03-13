@echo off
REM =============================================================
REM Ollama LLM API — Smart Startup Script (Windows)
REM Auto-detects NVIDIA GPU and enables GPU passthrough if found
REM =============================================================

echo.
echo ==========================================
echo    Ollama LLM API — Starting Up
echo ==========================================
echo.

REM ----- Step 1: Detect NVIDIA GPU -----
set GPU_DETECTED=false
set COMPOSE_FILES=-f docker-compose.yml

where nvidia-smi >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    nvidia-smi >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo [OK] NVIDIA GPU detected
        for /f "tokens=*" %%i in ('nvidia-smi --query-gpu=name --format=csv,noheader,nounits 2^>nul') do (
            echo      GPU: %%i
        )
        set GPU_DETECTED=true
    ) else (
        echo [!] nvidia-smi found but GPU not accessible
    )
) else (
    echo [!] No NVIDIA GPU detected
)

REM ----- Step 2: Check NVIDIA Container Toolkit -----
if "%GPU_DETECTED%"=="true" (
    docker info 2>nul | findstr /i "nvidia" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo [OK] NVIDIA Container Toolkit is installed
        set COMPOSE_FILES=-f docker-compose.yml -f docker-compose.gpu.yml
        echo [OK] GPU mode enabled
    ) else (
        echo [!] NVIDIA GPU found but Container Toolkit not installed
        echo     Install it: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html
        echo     Falling back to CPU mode
    )
)

if "%COMPOSE_FILES%"=="-f docker-compose.yml" (
    echo [i] Running in CPU-only mode
)

echo.

REM ----- Step 3: Start containers -----
echo Starting containers...
echo Command: docker compose %COMPOSE_FILES% up -d --build
echo.

docker compose %COMPOSE_FILES% up -d --build

echo.
echo ==========================================
echo    All services started!
echo ==========================================
echo.
echo   API:          http://localhost:8000
echo   Swagger Docs: http://localhost:8000/docs
echo   Ollama:       http://localhost:11434
echo   Health Check: http://localhost:8000/health
echo.
echo   Pull more models:  docker exec ollama ollama pull ^<model^>
echo   View logs:         docker compose %COMPOSE_FILES% logs -f
echo   Stop:              docker compose %COMPOSE_FILES% down
echo.
pause
