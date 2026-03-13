"""
Ollama Self-Hosted LLM API
- POST /ask : Send a question with optional structured data template
- GET  /models : List available Ollama models
"""

import time
import httpx
import psutil
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
import os
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

app = FastAPI(
    title="Ollama LLM API",
    description="Open API for self-hosted Ollama models with optional structured output",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Example templates — shown in Swagger docs and /examples endpoint
# ---------------------------------------------------------------------------
EXAMPLE_TEMPLATES = {
    "person_info": {
        "description": "Extract person information",
        "question": "Tell me about Elon Musk",
        "structure_template": {
            "name": "string",
            "age": "number",
            "nationality": "string",
            "occupation": "string",
            "summary": "string"
        }
    },
    "product_review": {
        "description": "Analyze a product review",
        "question": "Review the iPhone 15 Pro",
        "structure_template": {
            "product_name": "string",
            "rating": "number (1-10)",
            "pros": ["string"],
            "cons": ["string"],
            "verdict": "string"
        }
    },
    "translate": {
        "description": "Translate text with metadata",
        "question": "Translate 'Hello, how are you?' to Japanese, Thai, and French",
        "structure_template": {
            "original_text": "string",
            "original_language": "string",
            "translations": [
                {
                    "language": "string",
                    "translated_text": "string",
                    "romanization": "string"
                }
            ]
        }
    },
    "code_explanation": {
        "description": "Explain a piece of code",
        "question": "Explain what a Python decorator does",
        "structure_template": {
            "concept": "string",
            "explanation": "string",
            "example_code": "string",
            "use_cases": ["string"],
            "difficulty_level": "string (beginner/intermediate/advanced)"
        }
    },
    "comparison": {
        "description": "Compare two or more items",
        "question": "Compare Python vs JavaScript for backend development",
        "structure_template": {
            "items": ["string"],
            "criteria": [
                {
                    "name": "string",
                    "scores": {"item_name": "number (1-10)"},
                    "notes": "string"
                }
            ],
            "winner": "string",
            "conclusion": "string"
        }
    },
    "summary": {
        "description": "Summarize a topic",
        "question": "Summarize the history of artificial intelligence",
        "structure_template": {
            "title": "string",
            "key_points": ["string"],
            "timeline": [
                {
                    "year": "string",
                    "event": "string"
                }
            ],
            "conclusion": "string"
        }
    },
    "sentiment_and_data_extraction": {
        "model": "qwen3.5:0.8b",
        "temperature": 0.7,
        "question": "Analyze the sentiment and extract information from this article.",
        "structure_template":{ 
            "sentiment" : "sentiment of article.",       
            "word_and_scale":{
                "positive_word_with_scale" : [
                    {
                    "word":"the positive word extracted.",
                    "scale":"positive scale of word."
                    }
                ],
                "negative_word_with_scale" : [
                    {
                    "word":"the word extracted.",
                    "scale":"negative scale of word."
                    }
                ]
            }
        }
    }
}


class AskRequest(BaseModel):
    """Request body for the /ask endpoint."""
    question: str = Field(..., description="The question or prompt to send to the model")
    model: str = Field(default="llama3", description="Ollama model name to use")
    structure_template: Optional[dict] = Field(
        default=None,
        description=(
            "Optional JSON structure template. When provided, the model will be "
            "instructed to return its answer strictly in this format. "
            "See GET /examples for ready-to-use templates."
        ),
    )
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "What is Python?",
                    "model": "llama3",
                    "structure_template": None,
                    "temperature": 0.7
                },
                {
                    "question": "Tell me about Elon Musk",
                    "model": "llama3",
                    "structure_template": {
                        "name": "string",
                        "age": "number",
                        "nationality": "string",
                        "occupation": "string",
                        "summary": "string"
                    },
                    "temperature": 0.7
                },
                {
                    "question": "Analyze the sentiment and extract information from this article.",
                    "model": "qwen3.5:0.8b",
                    "temperature": 0.7,
                    "structure_template":{ 
                        "sentiment" : "sentiment of article.",       
                        "word_and_scale":{
                            "positive_word_with_scale" : [
                                {
                                "word":"the positive word extracted.",
                                "scale":"positive scale of word."
                                }
                            ],
                            "negative_word_with_scale" : [
                                {
                                "word":"the word extracted.",
                                "scale":"negative scale of word."
                                }
                            ]
                        }
                    }
                }
            ]
        }
    }

class ResourceUsage(BaseModel):
    """Resource usage metrics for a request."""
    total_duration_sec: float = Field(description="Total request duration in seconds")
    model_load_duration_sec: Optional[float] = Field(default=None, description="Time to load model into memory")
    prompt_eval_duration_sec: Optional[float] = Field(default=None, description="Time to evaluate the prompt")
    response_eval_duration_sec: Optional[float] = Field(default=None, description="Time to generate the response")
    tokens_per_second: Optional[float] = Field(default=None, description="Token generation speed")
    prompt_tokens: Optional[int] = Field(default=None, description="Number of tokens in the prompt")
    response_tokens: Optional[int] = Field(default=None, description="Number of tokens in the response")
    total_tokens: Optional[int] = Field(default=None, description="Total tokens (prompt + response)")
    cpu_usage_percent: Optional[float] = Field(default=None, description="CPU usage during request (%)")
    memory_used_mb: Optional[float] = Field(default=None, description="System memory used (MB)")
    memory_total_mb: Optional[float] = Field(default=None, description="System total memory (MB)")
    memory_usage_percent: Optional[float] = Field(default=None, description="System memory usage (%)")
    gpu_name: Optional[str] = Field(default=None, description="GPU name (if NVIDIA GPU detected)")
    gpu_usage_percent: Optional[float] = Field(default=None, description="GPU utilization (%) (if available)")
    gpu_memory_used_mb: Optional[float] = Field(default=None, description="GPU memory used (MB) (if available)")
    gpu_memory_total_mb: Optional[float] = Field(default=None, description="GPU total memory (MB) (if available)")
    gpu_memory_usage_percent: Optional[float] = Field(default=None, description="GPU memory usage (%) (if available)")


class AskResponse(BaseModel):
    """Response body for the /ask endpoint."""
    model: str
    question: str
    answer: str
    structured: bool = Field(description="Whether a structure template was applied")
    resource_usage: ResourceUsage = Field(description="Resource usage metrics for this request")

class ModelInfo(BaseModel):
    name: str
    size: Optional[str] = None
    modified_at: Optional[str] = None

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_prompt(question: str, structure_template: Optional[dict]) -> str:
    """Build the final prompt, injecting format instructions if a template is given."""
    if structure_template is None:
        return question

    template_str = _dict_to_schema_description(structure_template)

    return (
        f"{question}\n\n"
        f"---\n"
        f"IMPORTANT: You MUST respond ONLY with valid JSON that matches exactly this structure:\n"
        f"{template_str}\n"
        f"Do NOT include any explanation, markdown, or text outside the JSON object.\n"
        f"Fill every field with the appropriate value based on the question above."
    )


def _dict_to_schema_description(template: dict, indent: int = 0) -> str:
    """Convert a template dict into a readable schema description."""
    import json
    return json.dumps(template, indent=2, ensure_ascii=False)


def _get_gpu_info() -> dict:
    """Try to get NVIDIA GPU stats via nvidia-smi."""
    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=name,utilization.gpu,memory.used,memory.total",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            line = result.stdout.strip().split("\n")[0]
            parts = [p.strip() for p in line.split(",")]
            if len(parts) == 4:
                gpu_mem_used = float(parts[2])
                gpu_mem_total = float(parts[3])
                return {
                    "gpu_name": parts[0],
                    "gpu_usage_percent": float(parts[1]),
                    "gpu_memory_used_mb": gpu_mem_used,
                    "gpu_memory_total_mb": gpu_mem_total,
                    "gpu_memory_usage_percent": round(gpu_mem_used / gpu_mem_total * 100, 1) if gpu_mem_total > 0 else None,
                }
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        pass
    return {}


def _get_system_resources() -> dict:
    """Get CPU and memory usage."""
    try:
        mem = psutil.virtual_memory()
        return {
            "cpu_usage_percent": psutil.cpu_percent(interval=0.1),
            "memory_used_mb": round(mem.used / (1024 ** 2), 1),
            "memory_total_mb": round(mem.total / (1024 ** 2), 1),
            "memory_usage_percent": mem.percent,
        }
    except Exception:
        return {}


def _nanosec_to_sec(ns: Optional[int]) -> Optional[float]:
    """Convert nanoseconds to seconds, rounded to 3 decimal places."""
    if ns is None or ns == 0:
        return None
    return round(ns / 1_000_000_000, 3)

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/models", summary="List available Ollama models", response_model=list[ModelInfo])
async def list_models():
    """Fetch the list of models currently available in the local Ollama instance."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            resp.raise_for_status()
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Cannot connect to Ollama. Is it running?")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    data = resp.json()
    models = []
    for m in data.get("models", []):
        size_bytes = m.get("size", 0)
        size_str = f"{size_bytes / (1024**3):.1f} GB" if size_bytes else None
        models.append(ModelInfo(
            name=m.get("name", "unknown"),
            size=size_str,
            modified_at=m.get("modified_at"),
        ))
    return models

@app.get("/examples", summary="List example structure templates")
async def get_examples():
    """
    Returns a collection of ready-to-use structure_template examples.

    Copy any template and use it in the POST /ask endpoint.
    """
    return EXAMPLE_TEMPLATES

@app.post("/ask", summary="Ask a question to an Ollama model", response_model=AskResponse)
async def ask(req: AskRequest):
    """
    Send a question to the specified Ollama model.

    - If **structure_template** is provided, the model is instructed to respond
      strictly in that JSON format.
    - If **structure_template** is omitted or null, the model answers freely.
    """
    prompt = _build_prompt(req.question, req.structure_template)

    payload = {
        "model": req.model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": req.temperature,
        },
    }

    # If structure_template is provided, also pass format=json to Ollama
    if req.structure_template is not None:
        payload["format"] = "json"

    # ---- Measure time & resources ----
    start_time = time.time()

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
            resp.raise_for_status()
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Cannot connect to Ollama. Is it running?")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    total_duration = round(time.time() - start_time, 3)

    data = resp.json()
    answer = data.get("response", "").strip()

    # ---- Extract Ollama timing metrics (nanoseconds → seconds) ----
    prompt_tokens = data.get("prompt_eval_count")
    response_tokens = data.get("eval_count")
    eval_duration_ns = data.get("eval_duration")
    tokens_per_sec = None
    if response_tokens and eval_duration_ns and eval_duration_ns > 0:
        tokens_per_sec = round(response_tokens / (eval_duration_ns / 1_000_000_000), 1)

    # ---- Collect system & GPU resources ----
    try:
        sys_resources = _get_system_resources()
    except Exception:
        sys_resources = {}
    try:
        gpu_info = _get_gpu_info()
    except Exception:
        gpu_info = {}

    resource_usage = ResourceUsage(
        total_duration_sec=total_duration,
        model_load_duration_sec=_nanosec_to_sec(data.get("load_duration")),
        prompt_eval_duration_sec=_nanosec_to_sec(data.get("prompt_eval_duration")),
        response_eval_duration_sec=_nanosec_to_sec(eval_duration_ns),
        tokens_per_second=tokens_per_sec,
        prompt_tokens=prompt_tokens,
        response_tokens=response_tokens,
        total_tokens=(prompt_tokens or 0) + (response_tokens or 0) if prompt_tokens or response_tokens else None,
        **sys_resources,
        **gpu_info,
    )

    return AskResponse(
        model=req.model,
        question=req.question,
        answer=answer,
        structured=req.structure_template is not None,
        resource_usage=resource_usage,
    )


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", summary="Health check")
async def health():
    """Check if the API and Ollama are reachable."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            resp.raise_for_status()
        return {"status": "ok", "ollama": "connected"}
    except Exception:
        return {"status": "degraded", "ollama": "unreachable"}


# ---------------------------------------------------------------------------
# Run with: uvicorn app:app --host 0.0.0.0 --port 8000 --reload
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
