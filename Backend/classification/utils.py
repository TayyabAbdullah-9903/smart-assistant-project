from chatbot.gemini_utils import call_gemini_text

def infer_pi_class(procedure_text: str) -> dict:
    """
    Uses Gemini to generate PI-Class metadata from a manual section or query.
    """
    prompt = f"""
You are an automotive manual information analyst.

Given the following text, classify it according to the PI-Class schema:

1. Intrinsic Product Class — the actual physical or software component being described.
2. Extrinsic Product Class — the context, external factors, or environment interacting with it.
3. Intrinsic Information Class — the type of information (diagnostic, procedural, descriptive, etc.).
4. Extrinsic Information Class — how the information is presented (warning, symbol, display, etc.).

Respond strictly in JSON with these keys:
intrinsic_product, extrinsic_product, intrinsic_information, extrinsic_information.
Text:
{procedure_text}
"""

    result = call_gemini_text(prompt, model="gemini-2.0-flash", temperature=0.0, max_output_tokens=200)
    try:
        import json
        return json.loads(result)
    except Exception:
        return {
            "intrinsic_product": None,
            "extrinsic_product": None,
            "intrinsic_information": None,
            "extrinsic_information": None,
        }
