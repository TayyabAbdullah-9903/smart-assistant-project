import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from parser.models import ManualText
from django.conf import settings

def find_relevant_text(manual, query: str, top_n=3):
    """
    Uses Gemini embeddings to semantically find the most relevant manual sections.
    Falls back to keyword search if embeddings fail.
    """
    try:
        genai.configure(api_key=getattr(settings, "GOOGLE_API_KEY", None))
        embed_model = "models/embedding-001"

        # Get all pages
        pages = list(ManualText.objects.filter(manual=manual).values("text", "page_index"))
        if not pages:
            return ""

        texts = [p["text"] for p in pages]

        # Embed query
        query_vec = genai.embed_content(model=embed_model, content=query)["embedding"]

        # Embed all pages
        page_vecs = [genai.embed_content(model=embed_model, content=t)["embedding"] for t in texts]

        # Compute cosine similarity
        sims = cosine_similarity([query_vec], page_vecs)[0]
        top_indices = sims.argsort()[-top_n:][::-1]

        # Return top results
        top_texts = [texts[i] for i in top_indices if sims[i] > 0.1]
        if not top_texts:
            top_texts = [texts[i] for i in top_indices]

        return "\n\n".join(top_texts)

    except Exception as e:
        print("Embedding retrieval failed:", e)
        # fallback to simple keyword search
        from re import findall
        q_words = [w.lower() for w in findall(r"\w+", query)]
        texts = ManualText.objects.filter(manual=manual)
        scored = []
        for t in texts:
            txt = t.text.lower()
            score = sum(txt.count(w) for w in q_words)
            scored.append((score, t))
        scored.sort(key=lambda x: x[0], reverse=True)
        selected_texts = [t.text for score, t in scored[:top_n] if score > 0]
        if not selected_texts:
            selected_texts = [t.text for t in texts[:top_n]]
        return "\n\n".join(selected_texts)
