from llm.groq_client import structure_with_llama

def structurize_website_data(raw_data: dict) -> dict:
    """
    Converts the raw website data dict to a string (ensuring all values are JSON serializable) and sends it to Groq Llama-3-70B for structuring.
    Returns the structured dict.
    """
    import json
    def make_serializable(obj):
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_serializable(i) for i in obj]
        elif hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            return str(obj)

    serializable_data = make_serializable(raw_data)
    raw_text = json.dumps(serializable_data, indent=2, ensure_ascii=False)
    prompt = (
        "You are an expert data extractor. Given the following website data, return ONLY a valid JSON object with all relevant fields, categories, and values. Do not include any explanation or markdown, just the JSON."
    )
    return structure_with_llama(raw_text, system_prompt=prompt)
