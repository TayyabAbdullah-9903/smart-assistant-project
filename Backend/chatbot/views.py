# chatbot/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from manuals.models import Manual
from chatbot.models import ChatQuery
from parser.retriever import find_relevant_text
from chatbot.prompts import build_puml_prompt, build_explanation_prompt
from chatbot.gemini_utils import call_gemini_text
from uml.utils import render_plantuml_url
from classification.utils import infer_pi_class
from classification.models import PIClassification
from chatbot.file_utils import save_code_files
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
import requests, json
from datetime import datetime


@api_view(["POST"])
def query_chatbot(request):
    manual_id = request.data.get("manual_id")
    query = request.data.get("query")
    user_type = request.data.get("user_type", "user")

    # STEP 1: Identify user type automatically
    role_prompt = f"""
You are a classifier.

Classify the speaker of the following message as either:
- "technician" if it contains technical, diagnostic, or mechanical terms,
- "user" if it sounds like a casual car owner or general question.

User message:
{query}

Answer ONLY with either "technician" or "user".
"""
    user_type = call_gemini_text(role_prompt, model="gemini-2.0-flash", temperature=0.0, max_output_tokens=10)
    user_type = user_type.strip().lower()
    if user_type not in ["technician", "user"]:
        user_type = "user"

    # STEP 2: Determine UML diagram type
    type_prompt = f"""
You are an assistant that chooses UML diagram types.

Given this user request or text from a car manual, decide which UML diagram best represents it.
Possible types: activity, sequence, usecase, class, state, component.

User Query:
{query}

Answer ONLY with one word (the diagram type).
"""
    diagram_type = call_gemini_text(type_prompt, model="gemini-2.0-flash", temperature=0.0, max_output_tokens=20)
    diagram_type = diagram_type.strip().lower()
    if diagram_type not in ["activity", "sequence", "usecase", "class", "state", "component"]:
        diagram_type = "activity"  # fallback default

    # Validation
    if not manual_id or not query:
        return Response({"error": "manual_id and query are required."}, status=400)

    manual = Manual.objects.filter(id=manual_id).first()
    if not manual:
        return Response({"error": "Manual not found."}, status=404)

    # STEP 3: Retrieve relevant text
    procedure_text = clean_text(find_relevant_text(manual, query))
    print("\n=== MANUAL DEBUG INFO ===")
    print("Manual Name:", manual.name if hasattr(manual, "name") else manual.id)
    print("Query:", query)
    print("Retrieved Text Preview:\n", procedure_text[:1000])
    print("==========================\n")

    if not procedure_text or not procedure_text.strip():
        return Response({
            "error": "No relevant content found in the manual for this query.",
            "manual_id": manual.id,
            "query": query
        }, status=400)

    # STEP 4: Build UML prompt and call Gemini
    puml_prompt = build_puml_prompt(diagram_type, procedure_text)
    print("\n==========================")
    print("PUML PROMPT SENT TO GEMINI:")
    print(repr(puml_prompt[:1000]))
    print("==========================\n")

    puml_code = call_gemini_text(
        prompt_text=puml_prompt,
        model="gemini-2.5-pro",
        temperature=0.7,
        max_output_tokens=1200
    )
    print(puml_code)

    # STEP 5: Render UML image
    try:
        image_url = render_plantuml_url(puml_code)
        print(image_url)
    except Exception as e:
        print("UML render failed:", e)
        image_url = None

    # STEP 6: Explanation generation
    explanation_prompt = build_explanation_prompt(user_type, procedure_text)
    print("\n=== EXPLANATION PROMPT SENT ===\n", explanation_prompt[:800], "\n=========================\n")

    explanation = call_gemini_text(
        prompt_text=explanation_prompt,
        model="gemini-2.0-flash",
        temperature=0.7,
        max_output_tokens=600
    )
    print(explanation)

    # STEP 7: Save ChatQuery
    q = ChatQuery.objects.create(
        manual=manual,
        query_text=query,
        user_type=user_type,
        response_text=explanation,
        uml_code=puml_code,
        diagram_url=image_url
    )

    # STEP 8: Save UML code files (.puml, .txt, .py)
    files = save_code_files(q, puml_code, diagram_type)

    # Build absolute URLs
    request_scheme = "https" if request.is_secure() else "http"
    current_site = get_current_site(request)
    base_url = f"{request_scheme}://{current_site.domain}"

    puml_file_url = f"{base_url}{files['puml_path']}" if files.get("puml_path") else None
    py_file_url = f"{base_url}{files['py_path']}" if files.get("py_path") else None
    txt_file_url = f"{base_url}{files['txt_path']}" if files.get("txt_path") else None
    uml_file_url  = puml_file_url  # for backward compatibility

    # STEP 9: PI Classification
    pi_data = infer_pi_class(procedure_text)
    intrinsic_product = pi_data.get("intrinsic_product")
    extrinsic_product = pi_data.get("extrinsic_product")
    intrinsic_information = pi_data.get("intrinsic_information")
    extrinsic_information = pi_data.get("extrinsic_information")

    pi = PIClassification.objects.create(
        manual=manual,
        query=q,
        intrinsic_product=intrinsic_product,
        extrinsic_product=extrinsic_product,
        intrinsic_information=intrinsic_information,
        extrinsic_information=extrinsic_information,
    )

    # STEP 10: Simplify PI classification
    pi_summary_prompt = f"""
You are an automotive domain classifier.

Given this PI-Class metadata, summarize it into one of these top-level categories:
Maintenance, Safety, Diagnostics, Indicators, Controls, Electrical, Engine, Transmission, Other.

Return only one of those words, nothing else.

PI-Class JSON:
{json.dumps(pi_data, indent=2)}
"""
    pi_class_simple = call_gemini_text(
        prompt_text=pi_summary_prompt,
        model="gemini-2.0-flash",
        temperature=0.0,
        max_output_tokens=10
    ).strip()

    # STEP 11: Log to Zapier
    log_to_zapier({
        "manual_id": manual.id,
        "query": query,
        "user_type": user_type,
        "diagram_type": diagram_type,
        "pi_class": pi_class_simple,
        "intrinsic_product": intrinsic_product,
        "extrinsic_product": extrinsic_product,
        "intrinsic_info": intrinsic_information,
        "extrinsic_info": extrinsic_information,
        "response": explanation,
        "uml_image": image_url,
        "uml_file_url": uml_file_url,
        "feedback": "Good"
    })

    # STEP 12: Return response
    return Response({
        "response": explanation,
        "uml_code": puml_code,
        "user_type": user_type,
        "diagram_type": diagram_type,
        "uml_image": image_url,
        "pi_class": pi_class_simple,
        "intrinsic_product": intrinsic_product,
        "extrinsic_product": extrinsic_product,
        "intrinsic_info": intrinsic_information,
        "extrinsic_info": extrinsic_information,
        "query_id": q.id,
        "puml_file_url": puml_file_url,
        "feedback": "Good"
    })


def clean_text(t: str) -> str:
    import re
    if not t:
        return ""
    t = re.sub(r"[^\x20-\x7E\n]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def log_to_zapier(data):
    ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/25069512/uriqugw/"  # Replace with your actual Zapier URL
    try:
        print(data)
        payload = {
            "timestamp": datetime.now().isoformat(),
            "manual_id": data.get("manual_id"),
            "query": data.get("query"),
            "user_type": data.get("user_type"),
            "diagram_type": data.get("diagram_type"),
            "pi_class": data.get("pi_class"),
            "intrinsic_product": data.get("intrinsic_product"),
            "extrinsic_product": data.get("extrinsic_product"),
            "intrinsic_info": data.get("intrinsic_info"),
            "extrinsic_info": data.get("extrinsic_info"),
            "response": data.get("response"),
            "uml_image": data.get("uml_image"),
            "uml_file_url": data.get("uml_file_url"),
            "feedback": data.get("feedback"),
        }
        requests.post(ZAPIER_WEBHOOK_URL, json=payload)
    except Exception as e:
        print("Zapier logging failed:", e)
