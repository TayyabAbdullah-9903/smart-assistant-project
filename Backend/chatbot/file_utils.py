# chatbot/file_utils.py
import os
from django.conf import settings
from django.core.files import File

def save_code_files(chat_query, puml_code: str, diagram_type: str):
    """
    Save .puml, .txt, and .py code files for a ChatQuery.
    Returns relative MEDIA_URL paths.
    """
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "uml_code"), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "uml_code_py"), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "uml_code_txt"), exist_ok=True)

    base_name = f"query_{chat_query.id}_{diagram_type}"
    puml_path = os.path.join(settings.MEDIA_ROOT, "uml_code", f"{base_name}.puml")
    txt_path = os.path.join(settings.MEDIA_ROOT, "uml_code_txt", f"{base_name}.txt")
    py_path = os.path.join(settings.MEDIA_ROOT, "uml_code_py", f"{base_name}.py")

    with open(puml_path, "w", encoding="utf-8") as f:
        f.write(puml_code)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(puml_code)
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(generate_py_template(diagram_type, puml_code))

    from django.core.files import File
    with open(puml_path, "rb") as f:
        chat_query.puml_file.save(os.path.basename(puml_path), File(f), save=False)
    with open(txt_path, "rb") as f:
        chat_query.txt_file.save(os.path.basename(txt_path), File(f), save=False)
    with open(py_path, "rb") as f:
        chat_query.py_file.save(os.path.basename(py_path), File(f), save=False)

    chat_query.save()

    return {
        "puml_path": f"{settings.MEDIA_URL}uml_code/{base_name}.puml",
        "txt_path": f"{settings.MEDIA_URL}uml_code_txt/{base_name}.txt",
        "py_path": f"{settings.MEDIA_URL}uml_code_py/{base_name}.py",
    }


def generate_py_template(diagram_type: str, puml_code: str) -> str:
    """Generate a minimal Python rendering script for Colab."""
    import textwrap
    return textwrap.dedent(f"""
    \"\"\"Auto-generated UML rendering script
    Diagram type: {diagram_type}
    \"\"\"

    PLANTUML_SOURCE = r\"\"\"{puml_code}\"\"\"

    import re, networkx as nx, matplotlib.pyplot as plt
    from graphviz import Source

    def extract_edges(puml_text):
        edges = []
        for line in puml_text.splitlines():
            line = line.strip()
            m = re.match(r'\"?([^\"\\(]+)\"?\\s*-+>+\\s*\"?([^\"\\)]+)\"?', line)
            if m:
                edges.append(m.groups())
        return edges

    edges = extract_edges(PLANTUML_SOURCE)
    G = nx.DiGraph()
    G.add_edges_from(edges)
    nx.draw_networkx(G, with_labels=True, node_color='lightblue', node_size=2500, arrows=True)
    plt.axis('off')
    plt.show()
    """)
