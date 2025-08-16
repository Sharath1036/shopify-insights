
import os
from dotenv import load_dotenv
import groq
import json as pyjson

load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

groq_client = groq.Groq(api_key=GROQ_API_KEY)

def structure_with_llama(raw_text: str, system_prompt: str = None) -> dict:
    """
    Sends the raw text to Groq's Llama-3-70B Versatile model and returns the structured response using response_format with json_schema.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in environment variables.")
    prompt = system_prompt or (
        "You are an expert data extractor. Structure the following website data into a clean, detailed JSON object with all relevant fields, categories, and values."
    )
    # Generic schema: let the model decide, but require valid JSON
    schema = {
        "type": "object"
    }
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": raw_text}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "website_structured_data",
                "schema": schema
            }
        },
        temperature=0.2
    )
    content = response.choices[0].message.content
    try:
        return pyjson.loads(content)
    except Exception:
        return {"raw": content}
