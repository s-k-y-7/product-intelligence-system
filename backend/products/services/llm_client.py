import os
import json
from groq import Groq
from typing import Dict, Any

class GroqClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            self.configured = False
        else:
            self.client = Groq(api_key=api_key)
            self.model = "llama-3.3-70b-versatile"
            self.configured = True

    def extract_insight(self, text: str) -> Dict[str, Any]:
        """
        Takes raw review text or video transcript and extracts structured JSON insights.
        """
        if not self.configured:
            raise ValueError("GROQ_API_KEY is not configured or is using the placeholder.")

        prompt = f"""
You are an expert product analyst. I will provide you with a product review or video transcript.
Please analyze it and extract key insights. 

Return ONLY a valid JSON object matching exactly this schema:
{{
    "pros_summary": ["short string", "short string"],
    "cons_summary": ["short string", "short string"],
    "common_complaints": ["short string"],
    "verdict": "A 1-2 sentence final verdict on the product based on this text.",
    "confidence": 0.9
}}

If there are no clear pros, cons, or complaints, return empty arrays.

TEXT TO ANALYZE:
{text}
"""
        
        try:
            # We enforce JSON response via response_format
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.2, # Keep it deterministic and factual
                response_format={"type": "json_object"}
            )
            
            # The model should return valid JSON as a string
            result_json = json.loads(response.choices[0].message.content)
            return result_json
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from Groq response: {response.choices[0].message.content}") from e
        except Exception as e:
            raise Exception(f"Groq API error: {e}")
