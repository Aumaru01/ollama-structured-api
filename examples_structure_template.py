"""
Example templates for structured output.

Each template shows a ready-to-use structure_template that can be sent
to POST /ask.  Import EXAMPLE_TEMPLATES in app.py so the /examples
endpoint stays clean while the main file stays short.
"""

# ---------------------------------------------------------------------------
# Ready-to-use structure templates — exposed via GET /examples
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
        "question": "Analyze the sentiment and extract information from this article: 'The quick brown fox jumps over the lazy dog'",
        "structure_template":{
            "summary": "brief summary of article.",
            "sentiment" : "sentiment of article.",       
            "word_and_scale":{
                "positive_word_with_scale" : [
                    {
                    "word":"the positive word extracted.",
                    "score":"positive score of word.(1-5)"
                    }
                ],
                "negative_word_with_scale" : [
                    {
                    "word":"the word extracted.",
                    "score":"negative score of word.(1-5)"
                    }
                ]
            }
        }
    },
    "insight_extraction": {
        "description": "Extract insights from a text",
        "question": "Extract key insights from this market research report.",
        "structure_template": {
            "report_title": "string",
            "key_insights": [
                {
                    "insight": "string",
                    "confidence": "number (0-1)",
                    "source_text": "string"
                }
            ]
        }
    }
}

# ---------------------------------------------------------------------------
# Swagger examples for AskRequest (shown in POST /ask docs)
# ---------------------------------------------------------------------------
ASK_REQUEST_EXAMPLES = [
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
        "question": "Analyze the sentiment and extract information from this article: 'The quick brown fox jumps over the lazy dog'",
        "model": "qwen3.5:0.8b",
        "temperature": 0.7,
        "structure_template": {
            "summary": "brief summary of article.",
            "sentiment": "sentiment of article.",
            "word_and_scale": {
                "positive_word_with_scale": [
                    {
                        "word": "the positive word extracted.",
                        "score": "positive score of word.(1-5)"
                    }
                ],
                "negative_word_with_scale": [
                    {
                        "word": "the word extracted.",
                        "score": "negative score of word.(1-5)"
                    }
                ]
            }
        }
    }
]
