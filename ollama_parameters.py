"""
Ollama model parameters reference.

A static list of all tuning parameters that Ollama accepts in the
`options` object.  Imported by app.py and served via GET /parameter_available.
"""

OLLAMA_PARAMETERS = [
    {
        "name": "temperature",
        "type": "float",
        "default": 0.8,
        "range": "0.0 – 2.0",
        "description": (
            "Controls randomness of the output. "
            "Higher values (e.g. 1.5) produce more creative results; "
            "lower values (e.g. 0.2) make output more focused and deterministic."
        ),
    },
    {
        "name": "top_p",
        "type": "float",
        "default": 0.9,
        "range": "0.0 – 1.0",
        "description": (
            "Nucleus sampling — only tokens whose cumulative probability "
            "reaches top_p are considered. Lower values narrow the token pool."
        ),
    },
    {
        "name": "top_k",
        "type": "int",
        "default": 40,
        "range": "1 – ∞",
        "description": (
            "Limits the next-token candidates to the top K most probable tokens. "
            "Lower values reduce randomness; 1 = greedy decoding."
        ),
    },
    {
        "name": "num_ctx",
        "type": "int",
        "default": 2048,
        "range": "model-dependent",
        "description": (
            "Context window size in tokens. Determines how much text the model "
            "can see at once. Larger values need more memory."
        ),
    },
    {
        "name": "num_predict",
        "type": "int",
        "default": -1,
        "range": "-2, -1, or 1 – ∞",
        "description": (
            "Maximum number of tokens to generate. "
            "-1 = infinite (stop on EOS), -2 = fill the context window."
        ),
    },
    {
        "name": "repeat_penalty",
        "type": "float",
        "default": 1.1,
        "range": "0.0 – 2.0",
        "description": (
            "Penalises tokens that have already appeared, reducing repetition. "
            "Values > 1 discourage repeats; 1.0 = no penalty."
        ),
    },
    {
        "name": "repeat_last_n",
        "type": "int",
        "default": 64,
        "range": "0 – num_ctx",
        "description": (
            "How many recent tokens to consider for the repeat penalty. "
            "0 = disabled, -1 = use full context (num_ctx)."
        ),
    },
    {
        "name": "seed",
        "type": "int",
        "default": 0,
        "range": "any integer",
        "description": (
            "Random seed for reproducibility. "
            "Set a specific value to get consistent outputs across runs. "
            "0 = random seed each time."
        ),
    },
    {
        "name": "stop",
        "type": "list[str]",
        "default": None,
        "range": "any strings",
        "description": (
            "Stop sequences — generation halts when any of these strings is produced. "
            'Example: ["\\n", "User:"]'
        ),
    },
    {
        "name": "tfs_z",
        "type": "float",
        "default": 1.0,
        "range": "0.0 – 1.0",
        "description": (
            "Tail-free sampling parameter. "
            "1.0 = disabled. Lower values cut low-probability tail tokens more aggressively."
        ),
    },
    {
        "name": "mirostat",
        "type": "int",
        "default": 0,
        "range": "0, 1, or 2",
        "description": (
            "Enable Mirostat sampling for perplexity control. "
            "0 = disabled, 1 = Mirostat v1, 2 = Mirostat v2."
        ),
    },
    {
        "name": "mirostat_tau",
        "type": "float",
        "default": 5.0,
        "range": "0.0 – 10.0",
        "description": (
            "Target perplexity for Mirostat. "
            "Lower values produce more focused text; higher values allow more variety."
        ),
    },
    {
        "name": "mirostat_eta",
        "type": "float",
        "default": 0.1,
        "range": "0.0 – 1.0",
        "description": (
            "Learning rate for Mirostat feedback. "
            "Controls how quickly the algorithm adjusts to meet the target perplexity."
        ),
    },
    {
        "name": "num_gpu",
        "type": "int",
        "default": -1,
        "range": "-1 – ∞",
        "description": (
            "Number of model layers to offload to GPU. "
            "-1 = auto-detect based on available VRAM. 0 = CPU only."
        ),
    },
    {
        "name": "num_thread",
        "type": "int",
        "default": 0,
        "range": "0 – CPU cores",
        "description": (
            "Number of CPU threads for inference. "
            "0 = auto-detect (typically uses half of available cores for best performance)."
        ),
    },
]
