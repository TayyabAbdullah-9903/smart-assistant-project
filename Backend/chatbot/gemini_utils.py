# chatbot/gemini_utils.py
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def call_gemini_text(prompt_text: str, model: str = "gemini-2.5-pro", temperature: float = 0.7, max_output_tokens: int = 1024):
    """
    Sends a text prompt to Gemini and returns generated text.
    Handles empty or filtered responses gracefully.
    """
    if not prompt_text or not prompt_text.strip():
        return "[Error] Empty prompt text provided."

    model_instance = genai.GenerativeModel(model)

    try:
        response = model_instance.generate_content(
            prompt_text,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens
            }
        )

        # Some responses may not contain parts if safety filter triggered
        if getattr(response, "prompt_feedback", None):
            if response.prompt_feedback.block_reason != 0:
                return f"[Safety Blocked] Gemini refused to respond. Reason: {response.prompt_feedback}"

        if hasattr(response, "text") and response.text:
            return response.text
        
        if hasattr(response, "prompt_feedback"):
            print("Prompt feedback:", response.prompt_feedback)

        # Fallback for candidate-based responses
        
        if hasattr(response, "candidates") and response.candidates:
            cand = response.candidates[0]
            if hasattr(cand, "content") and cand.content.parts:
                return cand.content.parts[0].text

        return "[No text returned by Gemini.]"

    except Exception as e:
        return f"[Gemini Error] {e}"
