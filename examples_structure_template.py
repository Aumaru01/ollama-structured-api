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
        "question": "วิเคราะห์ sentiment และ extract information จากข้อความนี้: '<div>กองกำลังป้องกัน &nbsp;อิสราเอล &nbsp;(IDF) ปฏิบัติการโจมตีทางอากาศในกรุงเตหะรานเมื่อช่วงข้ามคืนที่ผ่านมา (17 มี.ค.) โดยมีเป้าหมายหลักเพื่อปลิดชีพ เอสมาอิล คาติบ &nbsp;รัฐมนตรี &nbsp;ว่าการกระทรวงข่าวกรองของ &nbsp;อิหร่าน &nbsp;ซึ่งขณะนี้กองทัพ &nbsp;อิสราเอล &nbsp;กำลังเร่งประเมินผลการโจมตีดังกล่าว เพื่อยืนยันชะตากรรมของ &nbsp;รัฐมนตรี &nbsp;รายนี้อย่างเป็นทางการ</div><br /><div>ทั้งนี้ ปฏิบัติการดังกล่าวได้รับการยืนยันจากเจ้าหน้าที่ทางการของอิสราเอล ภายหลังจากที่สำนักข่าวอิหร่าน อินเตอร์เนชันแนล (Iran International) เป็นสื่อแรกที่รายงานข่าวการโจมตีนี้ออกไป</div><br /><ul><li>* *</li></ul>'",
        "structure_template": {
            "summary": "บทสรุปแบบย่อของบทความ",
            "sentiment": "sentiment ของบทความ",
            "word_and_score": {
                "positive_word_with_score": [
                    {
                        "word": "positive word extracted.",
                        "score": "positive score of word.(1-5)"
                    }
                ],
                "negative_word_with_score": [
                    {
                        "word": "negative word extracted.",
                        "score": "negative score of word.(1-5)"
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
    },

    # ----- Image / Vision examples -----
    "image_describe": {
        "description": "Describe an image in detail (requires vision model e.g. llava, moondream)",
        "question": "Describe this image in detail. What do you see?",
        "note": "Send base64-encoded image in the 'images' field, or use POST /ask_image to upload file directly",
        "structure_template": None,
        "required_model_type": "vision (e.g. llava:7b, moondream, bakllava, minicpm-v)"
    },
    "image_structured_analysis": {
        "description": "Analyze an image and return structured JSON output",
        "question": "Analyze this image and extract the information.",
        "note": "Send base64-encoded image in the 'images' field, or use POST /ask_image to upload file directly",
        "structure_template": {
            "description": "string - detailed description of the image",
            "objects_detected": ["string - list of objects visible in the image"],
            "colors": ["string - dominant colors in the image"],
            "scene_type": "string (indoor/outdoor/abstract/document/other)",
            "mood": "string - overall mood or atmosphere",
            "text_in_image": "string or null - any text visible in the image"
        },
        "required_model_type": "vision (e.g. llava:7b, moondream, bakllava, minicpm-v)"
    },
    "image_ocr": {
        "description": "Extract text from an image (OCR)",
        "question": "Read and extract all text from this image. Return the text exactly as it appears.",
        "note": "Send base64-encoded image in the 'images' field, or use POST /ask_image to upload file directly",
        "structure_template": {
            "extracted_text": "string - all text found in the image",
            "language": "string - detected language of the text",
            "confidence": "string (high/medium/low)"
        },
        "required_model_type": "vision (e.g. llava:7b, moondream, bakllava, minicpm-v)"
    },
    "image_comparison": {
        "description": "Compare two images (send 2 images in the images array)",
        "question": "Compare these two images. What are the similarities and differences?",
        "note": "Send 2 base64-encoded images in the 'images' field, or upload 2 files via POST /ask_image",
        "structure_template": {
            "image_1_description": "string",
            "image_2_description": "string",
            "similarities": ["string"],
            "differences": ["string"],
            "conclusion": "string"
        },
        "required_model_type": "vision (e.g. llava:7b, moondream, bakllava, minicpm-v)"
    },
    "image_food_analysis": {
        "description": "Analyze a food image and estimate nutrition",
        "question": "What food is in this image? Estimate the nutrition information.",
        "note": "Send base64-encoded image in the 'images' field, or use POST /ask_image to upload file directly",
        "structure_template": {
            "food_name": "string",
            "ingredients": ["string"],
            "estimated_calories": "number",
            "nutrition": {
                "protein_g": "number",
                "carbs_g": "number",
                "fat_g": "number"
            },
            "cuisine_type": "string",
            "is_healthy": "boolean"
        },
        "required_model_type": "vision (e.g. llava:7b, moondream, bakllava, minicpm-v)"
    }
}

# ---------------------------------------------------------------------------
# Swagger examples for AskRequest (shown in POST /ask docs)
# ---------------------------------------------------------------------------

# Placeholder base64 for documentation (1x1 red pixel PNG)
_SAMPLE_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg=="

ASK_IMAGE_REQUEST_EXAMPLES = [
    {
        "summary": "Describe an image (free-form answer)",
        "value": {
            "question": "What is in this image? Describe it in detail.",
            "model": "llava:7b",
            "images": [_SAMPLE_BASE64],
            "structure_template": None,
            "temperature": 0.7
        }
    },
    {
        "summary": "Analyze an image with structured output",
        "value": {
            "question": "Analyze this image and extract the information.",
            "model": "llava:7b",
            "images": [_SAMPLE_BASE64],
            "structure_template": {
                "description": "string",
                "objects_detected": ["string"],
                "colors": ["string"],
                "scene_type": "string (indoor/outdoor/abstract/document/other)",
                "mood": "string",
                "text_in_image": "string or null"
            },
            "temperature": 0.5
        }
    },
    {
        "summary": "OCR - extract text from image",
        "value": {
            "question": "Read and extract all text from this image.",
            "model": "llava:7b",
            "images": [_SAMPLE_BASE64],
            "structure_template": {
                "extracted_text": "string",
                "language": "string",
                "confidence": "string (high/medium/low)"
            },
            "temperature": 0.3
        }
    },
    {
        "summary": "Thai - วิเคราะห์รูปภาพอาหาร",
        "value": {
            "question": "อาหารในรูปนี้คืออะไร? วิเคราะห์ข้อมูลโภชนาการ",
            "model": "llava:7b",
            "images": [_SAMPLE_BASE64],
            "structure_template": {
                "food_name": "ชื่ออาหาร",
                "ingredients": ["วัตถุดิบ"],
                "estimated_calories": "number",
                "cuisine_type": "ประเภทอาหาร",
                "is_healthy": "boolean"
            },
            "temperature": 0.5
        }
    }
]

ASK_REQUEST_EXAMPLES = [
    {
        "model": "qwen3.5:0.8b",
        "temperature": 0.7,
        "question": "วิเคราะห์ sentiment และ extract information จากข้อความนี้: '<div>กองกำลังป้องกัน &nbsp;อิสราเอล &nbsp;(IDF) ปฏิบัติการโจมตีทางอากาศในกรุงเตหะรานเมื่อช่วงข้ามคืนที่ผ่านมา (17 มี.ค.) โดยมีเป้าหมายหลักเพื่อปลิดชีพ เอสมาอิล คาติบ &nbsp;รัฐมนตรี &nbsp;ว่าการกระทรวงข่าวกรองของ &nbsp;อิหร่าน &nbsp;ซึ่งขณะนี้กองทัพ &nbsp;อิสราเอล &nbsp;กำลังเร่งประเมินผลการโจมตีดังกล่าว เพื่อยืนยันชะตากรรมของ &nbsp;รัฐมนตรี &nbsp;รายนี้อย่างเป็นทางการ</div><br /><div>ทั้งนี้ ปฏิบัติการดังกล่าวได้รับการยืนยันจากเจ้าหน้าที่ทางการของอิสราเอล ภายหลังจากที่สำนักข่าวอิหร่าน อินเตอร์เนชันแนล (Iran International) เป็นสื่อแรกที่รายงานข่าวการโจมตีนี้ออกไป</div><br /><ul><li>* *</li></ul>'",
        "structure_template": {
            "summary": "บทสรุปแบบย่อของบทความ",
            "sentiment": "sentiment ของบทความ",
            "word_and_score": {
                "positive_word_with_score": [
                    {
                        "word": "positive word extracted.",
                        "score": "positive score of word.(1-5)"
                    }
                ],
                "negative_word_with_score": [
                    {
                        "word": "negative word extracted.",
                        "score": "negative score of word.(1-5)"
                    }
                ]
            }
        }
    },
    {
        "question": "What is Python?",
        "model": "qwen3.5:9b",
        "structure_template": None,
        "temperature": 0.7
    },
    {
        "question": "Tell me about Elon Musk",
        "model": "qwen3.5:9b",
        "structure_template": {
            "name": "string",
            "age": "number",
            "nationality": "string",
            "occupation": "string",
            "summary": "string"
        },
        "temperature": 0.7
    },
    # ----- Image / Vision examples -----
    {
        "question": "What is in this image? Describe it in detail.",
        "model": "llava:7b",
        "images": [_SAMPLE_BASE64],
        "structure_template": None,
        "temperature": 0.7
    },
    {
        "question": "Analyze this image and extract the information.",
        "model": "llava:7b",
        "images": [_SAMPLE_BASE64],
        "structure_template": {
            "description": "string",
            "objects_detected": ["string"],
            "colors": ["string"],
            "scene_type": "string (indoor/outdoor/abstract/document/other)",
            "text_in_image": "string or null"
        },
        "temperature": 0.5
    }
]
