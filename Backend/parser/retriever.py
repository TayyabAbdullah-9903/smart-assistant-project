import re
from parser.models import ManualText

def find_relevant_text(manual, query: str, top_n=3):
    texts = ManualText.objects.filter(manual=manual)
    q_words = [w.lower() for w in re.findall(r"\w+", query)]
    scored = []
    for t in texts:
        txt = t.text.lower()
        score = sum(txt.count(w) for w in q_words)
        scored.append((score, t))
    scored.sort(key=lambda x: x[0], reverse=True)
    selected_texts = [t.text for score,t in scored[:top_n] if score>0]
    if not selected_texts:
        selected_texts = [t.text for t in texts[:top_n]]
    return "\n\n".join(selected_texts)