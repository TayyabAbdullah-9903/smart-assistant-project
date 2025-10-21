import os
from datetime import datetime
from django.conf import settings

def save_uml_file(puml_code: str, query_id: int, diagram_type: str) -> str:
    """
    Saves UML code to a .puml file and returns the full public URL (not relative).
    """
    save_dir = os.path.join(settings.STATIC_ROOT, "uml_files")
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"query_{query_id}_{diagram_type}_{timestamp}.puml"
    full_path = os.path.join(save_dir, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(puml_code)

    # ✅ Build public URL using STATIC_URL and site domain
    # Fallback to localhost if SITE_URL not defined
    base_url = getattr(settings, "SITE_URL", "http://127.0.0.1:8000")
    public_url = f"{base_url}{settings.STATIC_URL}uml_files/{filename}"

    return public_url
