# Ollama Structured API

A FastAPI wrapper around [Ollama](https://ollama.com) that provides an open API for self-hosted LLM models with optional structured JSON output and resource usage monitoring.

![System Flowchart](flowchart.png)

## Features

- **Ask anything** — Send questions to any Ollama model via REST API
- **Structured output** — Optionally force the model to respond in a specific JSON structure
- **Model selection** — Choose from any model installed in your Ollama instance
- **Resource monitoring** — Every response includes CPU, memory, GPU usage, and token metrics
- **Auto GPU detection** — Startup script detects NVIDIA GPU and enables GPU passthrough
- **Centralized config** — Single `.env` file controls all ports, URLs, and defaults
- **Docker ready** — Run everything with a single command via Docker Compose
- **Swagger docs** — Interactive API documentation at `/docs`

## Project Structure

```
.
├── app.py                         # FastAPI application (main API code)
├── examples_structure_template.py # Example templates & Swagger examples
├── ollama_parameters.py           # Ollama parameter definitions
├── requirements.txt               # Python dependencies
├── .env                    # Configuration (ports, URLs, default model)
├── .env.example            # Configuration template
├── Dockerfile              # Container image for the API
├── docker-compose.yml      # Base Docker Compose (CPU mode)
├── docker-compose.gpu.yml  # GPU override (merged when NVIDIA detected)
├── start.sh                # Linux/macOS startup script (auto-detects GPU)
├── start.bat               # Windows startup script (auto-detects GPU)
├── flowchart.png           # System architecture flowchart
└── README.md               # This file
```

## Configuration

All settings are centralized in the `.env` file. Copy from the template and adjust:

```bash
cp .env.example .env
```

| Variable           | Default                    | Description                          |
|--------------------|----------------------------|--------------------------------------|
| `API_PORT`         | `8000`                     | Port for the FastAPI server          |
| `OLLAMA_PORT`      | `11434`                    | Port for the Ollama server           |
| `OLLAMA_BASE_URL`  | `http://localhost:11434`   | Ollama connection URL                |
| `DEFAULT_MODEL`    | `llama3`                   | Model to auto-pull on Docker startup |

Change any port once in `.env` — Docker, the API, and startup scripts all read from it automatically.

## Quick Start

### Option A: Direct (Ollama already installed)

```bash
# 1. Install Ollama: https://ollama.com/download
# 2. Pull a model
ollama pull llama3

# 3. Copy config and adjust if needed
cp .env.example .env

# 4. Install dependencies & run
pip install -r requirements.txt
python app.py
```

The API starts at `http://localhost:8000` (or whatever `API_PORT` you set in `.env`)

### Option B: Docker Compose

```bash
# 1. Copy config and adjust if needed
cp .env.example .env

# 2. Run (auto-detects GPU)
# Linux/macOS
chmod +x start.sh
./start.sh

# Windows
start.bat
```

The startup script automatically detects NVIDIA GPU, loads config from `.env`, and starts all services.

Or run manually:

```bash
# CPU only
docker compose up -d --build

# With GPU
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build
```

## API Endpoints

| Method | Endpoint      | Description                                      |
|--------|--------------|--------------------------------------------------|
| POST   | `/ask`       | Ask a question (supports text + base64 images)   |
| POST   | `/ask_image` | Ask with image file upload (multipart/form-data) |
| GET    | `/models`    | List available Ollama models                     |
| GET    | `/examples`  | Get example structure templates                  |
| GET    | `/health`    | Health check (API + Ollama connectivity)         |
| GET    | `/docs`      | Swagger UI (interactive API docs)                |

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

When you provide `structure_template`, the API does two things:
1. Sets Ollama's `format: "json"` to force valid JSON output
2. Injects format instructions into the prompt so the model matches your exact structure

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
      "word_and_score": {
        "positive_word_with_score": [
          { "word": "positive word", "score": "score 0-1" }
        ],
        "negative_word_with_score": [
          { "word": "negative word", "score": "score 0-1" }
        ]
      }
    }
  }'
```

### Image Input — base64 via `/ask`

Send base64-encoded images alongside your question. Requires a **vision-capable model** (e.g. `llava`, `llava-llama3`, `moondream`, `bakllava`, `minicpm-v`).

```bash
# Encode an image to base64
IMAGE_B64=$(base64 -w0 photo.jpg)   # Linux
IMAGE_B64=$(base64 -i photo.jpg)    # macOS

curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is in this image? Describe it in detail.",
    "model": "llava:7b",
    "images": ["'"$IMAGE_B64"'"]
  }'
```

With structured output:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Analyze this image and extract information.",
    "model": "llava:7b",
    "images": ["'"$IMAGE_B64"'"],
    "structure_template": {
      "description": "string",
      "objects_detected": ["string"],
      "colors": ["string"],
      "scene_type": "string (indoor/outdoor/abstract/document/other)",
      "text_in_image": "string or null"
    }
  }'
```

### Image Input — file upload via `/ask_image`

Upload image files directly using multipart/form-data (no base64 encoding needed):

```bash
# Single image
curl -X POST http://localhost:8000/ask_image \
  -F "question=What is in this image?" \
  -F "model=llava:7b" \
  -F "images=@photo.jpg"

# Multiple images
curl -X POST http://localhost:8000/ask_image \
  -F "question=Compare these two images" \
  -F "model=llava:7b" \
  -F "images=@photo1.jpg" \
  -F "images=@photo2.jpg"

# With structured output
curl -X POST http://localhost:8000/ask_image \
  -F "question=What food is this? Estimate nutrition." \
  -F "model=llava:7b" \
  -F 'structure_template={"food_name":"string","ingredients":["string"],"estimated_calories":"number"}' \
  -F "images=@food.jpg"
```

### List Models

```bash
curl http://localhost:8000/models
```

### View Example Templates

```bash
curl http://localhost:8000/examples
```

Available templates: `person_info`, `product_review`, `translate`, `code_explanation`, `comparison`, `summary`, `sentiment_and_data_extraction`, `insight_extraction`, `image_describe`, `image_structured_analysis`, `image_ocr`, `image_comparison`, `image_food_analysis`

## Request Parameters

| Parameter            | Type       | Required | Default    | Description                                         |
|---------------------|------------|----------|------------|-----------------------------------------------------|
| `question`          | string     | Yes      | -          | The question/prompt to send                         |
| `model`             | string     | No       | `"llama3"` | Ollama model name                                   |
| `structure_template`| dict       | No       | `null`     | JSON template to force structured output            |
| `images`            | list[str]  | No       | `null`     | Base64-encoded images (requires vision model)       |
| `temperature`       | float      | No       | `0.7`      | Sampling temperature (0.0 - 2.0)                    |

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

### Resource Usage Fields

| Field                      | Type   | Source       | Description                          |
|---------------------------|--------|--------------|--------------------------------------|
| `total_duration_sec`      | float  | Timer        | Total request wall-clock time        |
| `model_load_duration_sec` | float  | Ollama       | Time to load model into memory       |
| `prompt_eval_duration_sec`| float  | Ollama       | Time to process the prompt           |
| `response_eval_duration_sec`| float| Ollama       | Time to generate the response        |
| `tokens_per_second`       | float  | Calculated   | Token generation speed               |
| `prompt_tokens`           | int    | Ollama       | Number of prompt tokens              |
| `response_tokens`         | int    | Ollama       | Number of generated tokens           |
| `total_tokens`            | int    | Calculated   | prompt_tokens + response_tokens      |
| `cpu_usage_percent`       | float  | psutil       | System CPU usage (%)                 |
| `memory_used_mb`          | float  | psutil       | System RAM used (MB)                 |
| `memory_total_mb`         | float  | psutil       | System total RAM (MB)                |
| `memory_usage_percent`    | float  | psutil       | System RAM usage (%)                 |
| `gpu_name`                | string | nvidia-smi   | GPU name (null if no NVIDIA GPU)     |
| `gpu_usage_percent`       | float  | nvidia-smi   | GPU utilization (%)                  |
| `gpu_memory_used_mb`      | float  | nvidia-smi   | GPU VRAM used (MB)                   |
| `gpu_memory_total_mb`     | float  | nvidia-smi   | GPU total VRAM (MB)                  |
| `gpu_memory_usage_percent`| float  | nvidia-smi   | GPU VRAM usage (%)                   |

## How Structured Output Works

The `structure_template` feature combines two mechanisms:

1. **Ollama's `format: "json"`** — Forces the model to output valid JSON (built-in Ollama feature)
2. **Prompt injection** — The API appends instructions to your question telling the model to match your exact template structure

Without `structure_template`, the model answers freely in plain text. With it, the model is constrained to return JSON matching your specified fields.

**Note:** Smaller models (< 7B parameters) may struggle to follow structured output instructions reliably. Use 7B+ models for best results.

## Error Handling

| Status | Error                | When                                    |
|--------|---------------------|-----------------------------------------|
| 422    | Validation Error    | Invalid input (e.g., temperature > 2.0) |
| 503    | Service Unavailable | Cannot connect to Ollama                |
| 4xx/5xx| Ollama HTTP Error   | Forwarded from Ollama response          |

Resource collection (CPU, GPU) failures are handled gracefully — fields return `null` instead of crashing.

## Vision Models (for Image Input)

To use the image features, pull a vision-capable model:

```bash
ollama pull llava:7b
ollama pull moondream
ollama pull bakllava
ollama pull minicpm-v

# Docker
docker exec ollama ollama pull llava:7b
```

Supported image formats: PNG, JPEG, WebP, GIF

## Pull More Models

```bash
# If using Ollama directly
ollama pull mistral
ollama pull codellama
ollama pull qwen2.5:7b

# If using Docker
docker exec ollama ollama pull mistral
```

Then select the model via the `model` field in your API request.

## Import Custom GGUF Models

In addition to pulling models from the Ollama Library, you can import your own GGUF files (e.g. downloaded from Hugging Face) into Ollama.

### Method 1: Using a Modelfile (Recommended)

Create a file named `Modelfile` and specify the path to your GGUF file:

```Dockerfile
# Modelfile
FROM ./my-model-Q4_K_M.gguf

# (Optional) Set a default system prompt
SYSTEM """You are a helpful AI assistant."""

# (Optional) Set default parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
```

Then build it as an Ollama model:

```bash
# Create the model from the Modelfile
ollama create my-custom-model -f Modelfile

# Test it
ollama run my-custom-model "Hello!"

# Use it via the API
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is AI?",
    "model": "my-custom-model"
  }'
```

### Method 2: Quick One-Liner (for quick testing)

```bash
# Create a minimal Modelfile and build
echo 'FROM ./model.gguf' > Modelfile
ollama create test-model -f Modelfile
```

### Example: Download a GGUF from Hugging Face

```bash
# 1. Download the GGUF file (example: Typhoon2 Thai model)
wget https://huggingface.co/scb10x/typhoon2-8b-instruct-GGUF/resolve/main/typhoon2-8b-instruct.Q4_K_M.gguf

# 2. Create a Modelfile
cat > Modelfile <<'EOF'
FROM ./typhoon2-8b-instruct.Q4_K_M.gguf

TEMPLATE """{{- if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""

SYSTEM """You are a helpful AI assistant that can communicate in both Thai and English."""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 8192
PARAMETER stop "<|im_end|>"
EOF

# 3. Create the model in Ollama
ollama create typhoon2-8b -f Modelfile

# 4. Use it via the API
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain Machine Learning in simple terms",
    "model": "typhoon2-8b"
  }'
```

### Example: GGUF Vision Model (with image support)

Some GGUF models support vision (e.g. LLaVA). You need to specify the multimodal projector file:

```Dockerfile
# Modelfile for a vision GGUF model
FROM ./llava-v1.6-mistral-7b.Q4_K_M.gguf

# Specify the mmproj (multimodal projector) for vision
ADAPTER ./llava-v1.6-mistral-7b-mmproj-f16.gguf

TEMPLATE """[INST] {{ if .System }}{{ .System }} {{ end }}{{ .Prompt }} [/INST]"""

PARAMETER temperature 0.7
PARAMETER num_ctx 4096
```

```bash
ollama create my-llava -f Modelfile

# Use with the /ask_image endpoint
curl -X POST http://localhost:8000/ask_image \
  -F "question=What is in this image?" \
  -F "model=my-llava" \
  -F "images=@photo.jpg"
```

### Common Modelfile Parameters

| Parameter      | Description                                          | Example                  |
|---------------|------------------------------------------------------|--------------------------|
| `FROM`        | Path to the GGUF file (required)                     | `FROM ./model.gguf`     |
| `ADAPTER`     | LoRA adapter or mmproj file for vision models        | `ADAPTER ./lora.gguf`   |
| `TEMPLATE`    | Chat template format (ChatML, Llama, Mistral, etc.)  | See examples above       |
| `SYSTEM`      | Default system prompt                                | `SYSTEM """..."""`       |
| `PARAMETER`   | Set parameters (temperature, top_p, num_ctx, etc.)   | `PARAMETER num_ctx 8192` |
| `LICENSE`     | Specify the model's license                          | `LICENSE """MIT"""`      |

### Managing Created Models

```bash
# List all models
ollama list

# Show model details
ollama show my-custom-model

# Delete a model
ollama rm my-custom-model

# Copy a model (create an alias)
ollama cp my-custom-model my-model-v2
```

## Requirements

- Python 3.10+
- Ollama running locally (or via Docker)
- NVIDIA GPU + Container Toolkit (optional, for GPU acceleration)
- Docker & Docker Compose (optional, for containerized deployment)
