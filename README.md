# Ollama LLM Self-Hosted API

A FastAPI wrapper around [Ollama](https://ollama.com) that provides an open API for self-hosted LLM models with optional structured JSON output and resource usage monitoring.

## Features

- **Ask anything** — Send questions to any Ollama model via REST API
- **Structured output** — Optionally force the model to respond in a specific JSON structure
- **Model selection** — Choose from any model installed in your Ollama instance
- **Resource monitoring** — Every response includes CPU, memory, GPU usage, and token metrics
- **Auto GPU detection** — Startup script detects NVIDIA GPU and enables GPU passthrough
- **Docker ready** — Run everything with a single command via Docker Compose
- **Swagger docs** — Interactive API documentation at `/docs`

## Project Structure

```
.
├── app.py                  # FastAPI application (main API code)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image for the API
├── docker-compose.yml      # Base Docker Compose (CPU mode)
├── docker-compose.gpu.yml  # GPU override (merged when NVIDIA detected)
├── start.sh                # Linux/macOS startup script (auto-detects GPU)
├── start.bat               # Windows startup script (auto-detects GPU)
├── .env.example            # Environment variable template
└── README.md               # This file
```

## Quick Start

### Option A: Direct (Ollama already installed)

```bash
# 1. Install Ollama: https://ollama.com/download
# 2. Pull a model
ollama pull llama3

# 3. Install dependencies & run
pip install -r requirements.txt
python app.py
```

The API starts at `http://localhost:8000`

### Option B: Docker Compose

```bash
# Linux/macOS
chmod +x start.sh
./start.sh

# Windows
start.bat
```

The startup script auto-detects NVIDIA GPU. If found and NVIDIA Container Toolkit is installed, it enables GPU passthrough automatically.

Or run manually:

```bash
# CPU only
docker compose up -d --build

# With GPU
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build
```

## API Endpoints

| Method | Endpoint     | Description                              |
|--------|-------------|------------------------------------------|
| POST   | `/ask`      | Ask a question to an Ollama model        |
| GET    | `/models`   | List available Ollama models             |
| GET    | `/examples` | Get example structure templates          |
| GET    | `/health`   | Health check (API + Ollama connectivity) |
| GET    | `/docs`     | Swagger UI (interactive API docs)        |

## Usage Examples

### Simple Question (no structure)

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Python?",
    "model": "llama3"
  }'
```

### Structured Output (with template)

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Tell me about Elon Musk",
    "model": "llama3",
    "structure_template": {
      "name": "string",
      "age": "number",
      "nationality": "string",
      "occupation": "string",
      "summary": "string"
    }
  }'
```

### Sentiment Analysis (with template)

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Analyze the sentiment of: I love this product but the price is too high",
    "model": "llama3",
    "structure_template": {
      "sentiment": "overall sentiment",
      "word_and_scale": {
        "positive_word_with_scale": [
          { "word": "positive word", "scale": "scale 0-1" }
        ],
        "negative_word_with_scale": [
          { "word": "negative word", "scale": "scale 0-1" }
        ]
      }
    }
  }'
```

### List Models

```bash
curl http://localhost:8000/models
```

### View Example Templates

```bash
curl http://localhost:8000/examples
```

## Response Format

Every `/ask` response includes `resource_usage` metrics:

```json
{
  "model": "llama3",
  "question": "What is Python?",
  "answer": "Python is a high-level programming language...",
  "structured": false,
  "resource_usage": {
    "total_duration_sec": 2.345,
    "model_load_duration_sec": 0.102,
    "prompt_eval_duration_sec": 0.534,
    "response_eval_duration_sec": 1.709,
    "tokens_per_second": 48.3,
    "prompt_tokens": 15,
    "response_tokens": 82,
    "total_tokens": 97,
    "cpu_usage_percent": 45.2,
    "memory_used_mb": 8234.1,
    "memory_total_mb": 16384.0,
    "memory_usage_percent": 50.3,
    "gpu_name": "NVIDIA GeForce RTX 3060",
    "gpu_usage_percent": 87.0,
    "gpu_memory_used_mb": 4521.0,
    "gpu_memory_total_mb": 12288.0,
    "gpu_memory_usage_percent": 36.8
  }
}
```

## Request Parameters

| Parameter            | Type   | Required | Default  | Description                                  |
|---------------------|--------|----------|----------|----------------------------------------------|
| `question`          | string | Yes      | -        | The question/prompt to send                  |
| `model`             | string | No       | "llama3" | Ollama model name                            |
| `structure_template`| dict   | No       | null     | JSON template to force structured output     |
| `temperature`       | float  | No       | 0.7      | Sampling temperature (0.0 - 2.0)             |

## Configuration

| Environment Variable | Default                  | Description            |
|---------------------|--------------------------|------------------------|
| `OLLAMA_BASE_URL`   | `http://localhost:11434` | Ollama server address  |

## Pull More Models

```bash
# If using Ollama directly
ollama pull mistral
ollama pull codellama
ollama pull qwen2.5:7b

# If using Docker
docker exec ollama ollama pull mistral
```

## Requirements

- Python 3.10+
- Ollama running locally (or via Docker)
- NVIDIA GPU + Container Toolkit (optional, for GPU acceleration)
