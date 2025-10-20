from chatbot.gemini_utils import call_gemini_text
import re
import json

def infer_pi_class(procedure_text: str) -> dict:
    """
    Uses Gemini to generate PI-Class metadata from a manual section or query.
    """
    prompt = f"""
You are an **automotive manual information analyst**.

Your task is to classify the following vehicle-related text into the **PI-Class schema**.

Return your answer **ONLY as a compact valid JSON object**, without any explanations, notes, or markdown.

Schema:
{{
  "intrinsic_product": "<main vehicle component or subsystem>",
  "extrinsic_product": "<environmental or contextual factor>",
  "intrinsic_information": "<type of information — e.g., diagnostic, procedural, descriptive>",
  "extrinsic_information": "<presentation mode — e.g., warning, display, symbol, note>"
}}

Example output:
{{
  "intrinsic_product": "parking sensors",
  "extrinsic_product": "vehicle surroundings",
  "intrinsic_information": "diagnostic",
  "extrinsic_information": "warning"
}}

Now classify this text:
---
{procedure_text}
---
Respond **only with the JSON**.
"""

    import json
    result = call_gemini_text(prompt, model="gemini-2.0-flash", temperature=0.1, max_output_tokens=200)
    
    try:
        json_str = result.strip()
        # Attempt to extract JSON even if model wrapped it in prose
        match = re.search(r"\{.*\}", json_str, re.DOTALL)
        if match:
            json_str = match.group(0)
        return json.loads(json_str)
    except Exception as e:
        print("PI Classification parse error:", e, "Raw:", result)
        return {
            "intrinsic_product": "unknown",
            "extrinsic_product": "unknown",
            "intrinsic_information": "unknown",
            "extrinsic_information": "unknown",
        }
