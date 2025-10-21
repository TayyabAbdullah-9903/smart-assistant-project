import os
from datetime import datetime
from django.conf import settings

def save_uml_file(puml_code: str, query_id: int, diagram_type: str) -> str:
    """
    Saves UML code to a .puml file and returns the public URL.
    """
    # Ensure subfolder exists
    save_dir = os.path.join(settings.STATIC_ROOT, "uml_files")
    os.makedirs(save_dir, exist_ok=True)

    # Filename: query_<id>_<diagram_type>_<timestamp>.puml
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"query_{query_id}_{diagram_type}_{timestamp}.puml"
    full_path = os.path.join(save_dir, filename)

    # Write file
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(puml_code)

    # Public URL (assuming you serve static files at /static/)
    return f"{settings.STATIC_URL}uml_files/{filename}"
