# uml/utils.py
import zlib
import sys
from typing import Optional
import urllib.parse
from uml.utils_save import save_uml_file

# PlantUML uses a custom 6-bit encoding alphabet:
_ENCODE_TABLE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

def _deflate_and_strip(data: bytes) -> bytes:
    """
    Deflate (zlib compress) and strip zlib header (2 bytes) and checksum (4 bytes).
    This is the algorithm recommended by PlantUML docs.
    """
    compressed = zlib.compress(data)
    # strip zlib header and checksum (RFC1950 wrapper)
    # compress returns: 2-byte header + deflate data + 4-byte adler32 checksum
    if len(compressed) <= 6:
        # something wrong, return original compressed
        return compressed
    return compressed[2:-4]


def _encode6bit(b: int) -> str:
    return _ENCODE_TABLE[b & 0x3F]


def _append3bytes(b1: int, b2: int, b3: int) -> str:
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return _encode6bit(c1) + _encode6bit(c2) + _encode6bit(c3) + _encode6bit(c4)


def plantuml_encode(plantuml_text: str) -> str:
    """
    Correct PlantUML encoder:
    - UTF-8 encode,
    - zlib deflate (strip header & checksum),
    - custom 6-bit encode to produce the path component.
    """
    if isinstance(plantuml_text, str):
        data = plantuml_text.encode("utf-8")
    else:
        data = plantuml_text

    compressed = _deflate_and_strip(data)
    # Now perform 6-bit packing in groups of 3 bytes
    res = []
    i = 0
    length = len(compressed)
    while i < length:
        b1 = compressed[i]
        b2 = compressed[i + 1] if i + 1 < length else 0
        b3 = compressed[i + 2] if i + 2 < length else 0
        res.append(_append3bytes(b1, b2, b3))
        i += 3
    return "".join(res)


def render_plantuml_url(puml_text: str, server: str = "https://www.plantuml.com/plantuml/png/") -> str:
    """
    Build a PlantUML server URL that returns the PNG image.
    Ensures the input contains @startuml/@enduml and encodes correctly.
    """
    if not puml_text:
        raise ValueError("Empty PUML text")

    # Make sure puml_text contains @startuml/@enduml
    trimmed = puml_text.strip()
    # If the model returned extra commentary, try to extract the @startuml..@enduml block
    if "@startuml" in trimmed and "@enduml" in trimmed:
        start = trimmed.index("@startuml")
        end = trimmed.rindex("@enduml") + len("@enduml")
        core = trimmed[start:end]
    else:
        # If not found, assume the entire text is PUML; still try to encode
        core = trimmed

    # PlantUML server expects no URL encoding for the encoded blob (it is safe)
    encoded = plantuml_encode(core)
    return server + encoded


# --- convenience/test helpers ---
def validate_puml(puml_text: str) -> Optional[str]:
    """
    Quick validator: check for @startuml and @enduml and return a cleaned block or None.
    """
    if not puml_text:
        return None
    txt = puml_text.strip()
    if "@startuml" in txt and "@enduml" in txt:
        s = txt.index("@startuml")
        e = txt.rindex("@enduml") + len("@enduml")
        return txt[s:e]
    return None
