#!/bin/bash
# =============================================================
# Ollama LLM API — Smart Startup Script
# Auto-detects NVIDIA GPU and enables GPU passthrough if found
# =============================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ----- Load .env config -----
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo -e "${GREEN}[✓] Loaded config from .env${NC}"
else
    echo -e "${YELLOW}[!] No .env file found, using defaults${NC}"
fi

API_PORT="${API_PORT:-8000}"
OLLAMA_PORT="${OLLAMA_PORT:-11434}"
DEFAULT_MODEL="${DEFAULT_MODEL:-llama3}"

echo ""
echo "=========================================="
echo "   Ollama LLM API — Starting Up"
echo "=========================================="
echo ""
echo "  Config: API_PORT=${API_PORT} | OLLAMA_PORT=${OLLAMA_PORT} | MODEL=${DEFAULT_MODEL}"
echo ""

# ----- Step 1: Detect NVIDIA GPU -----
GPU_DETECTED=false
COMPOSE_FILES="-f docker-compose.yml"

if command -v nvidia-smi &> /dev/null; then
    if nvidia-smi &> /dev/null; then
        GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits 2>/dev/null | head -1)
        GPU_MEMORY=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
        GPU_DETECTED=true
        echo -e "${GREEN}[✓] NVIDIA GPU detected: ${GPU_NAME} (${GPU_MEMORY} MiB)${NC}"
    else
        echo -e "${YELLOW}[!] nvidia-smi found but GPU not accessible${NC}"
    fi
else
    echo -e "${YELLOW}[!] No NVIDIA GPU detected (nvidia-smi not found)${NC}"
fi

# ----- Step 2: Check NVIDIA Container Toolkit -----
if [ "$GPU_DETECTED" = true ]; then
    if docker info 2>/dev/null | grep -q "nvidia"; then
        echo -e "${GREEN}[✓] NVIDIA Container Toolkit is installed${NC}"
        COMPOSE_FILES="-f docker-compose.yml -f docker-compose.gpu.yml"
        echo -e "${GREEN}[✓] GPU mode enabled — Ollama will use your GPU${NC}"
    else
        echo -e "${YELLOW}[!] NVIDIA GPU found but Container Toolkit not installed${NC}"
        echo -e "${YELLOW}    Install it: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html${NC}"
        echo -e "${YELLOW}    Falling back to CPU mode${NC}"
    fi
fi

if [ "$COMPOSE_FILES" = "-f docker-compose.yml" ]; then
    echo -e "${YELLOW}[i] Running in CPU-only mode${NC}"
fi

echo ""

# ----- Step 3: Start containers -----
echo "Starting containers..."
echo -e "Command: docker compose ${COMPOSE_FILES} up -d --build"
echo ""

docker compose ${COMPOSE_FILES} up -d --build

echo ""
echo "=========================================="
echo -e "${GREEN}   All services started!${NC}"
echo "=========================================="
echo ""
echo "  API:          http://localhost:${API_PORT}"
echo "  Swagger Docs: http://localhost:${API_PORT}/docs"
echo "  Ollama:       http://localhost:${OLLAMA_PORT}"
echo "  Health Check: http://localhost:${API_PORT}/health"
echo ""
echo "  Pull more models:  docker exec ollama ollama pull <model>"
echo "  View logs:         docker compose ${COMPOSE_FILES} logs -f"
echo "  Stop:              docker compose ${COMPOSE_FILES} down"
echo ""
