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
            "word_and_scale": {
                "positive_word_with_scale": [
                    {
                        "word": "positive word extracted.",
                        "score": "positive score of word.(1-5)"
                    }
                ],
                "negative_word_with_scale": [
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
    }
}

# ---------------------------------------------------------------------------
# Swagger examples for AskRequest (shown in POST /ask docs)
# ---------------------------------------------------------------------------
ASK_REQUEST_EXAMPLES = [
    {
        "model": "qwen3.5:0.8b",
        "temperature": 0.7,
        "question": "วิเคราะห์ sentiment และ extract information จากข้อความนี้: '<div>กองกำลังป้องกัน &nbsp;อิสราเอล &nbsp;(IDF) ปฏิบัติการโจมตีทางอากาศในกรุงเตหะรานเมื่อช่วงข้ามคืนที่ผ่านมา (17 มี.ค.) โดยมีเป้าหมายหลักเพื่อปลิดชีพ เอสมาอิล คาติบ &nbsp;รัฐมนตรี &nbsp;ว่าการกระทรวงข่าวกรองของ &nbsp;อิหร่าน &nbsp;ซึ่งขณะนี้กองทัพ &nbsp;อิสราเอล &nbsp;กำลังเร่งประเมินผลการโจมตีดังกล่าว เพื่อยืนยันชะตากรรมของ &nbsp;รัฐมนตรี &nbsp;รายนี้อย่างเป็นทางการ</div><br /><div>ทั้งนี้ ปฏิบัติการดังกล่าวได้รับการยืนยันจากเจ้าหน้าที่ทางการของอิสราเอล ภายหลังจากที่สำนักข่าวอิหร่าน อินเตอร์เนชันแนล (Iran International) เป็นสื่อแรกที่รายงานข่าวการโจมตีนี้ออกไป</div><br /><ul><li>* *</li></ul>'",
        "structure_template": {
            "summary": "บทสรุปแบบย่อของบทความ",
            "sentiment": "sentiment ของบทความ",
            "word_and_scale": {
                "positive_word_with_scale": [
                    {
                        "word": "positive word extracted.",
                        "score": "positive score of word.(1-5)"
                    }
                ],
                "negative_word_with_scale": [
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
    }
]
