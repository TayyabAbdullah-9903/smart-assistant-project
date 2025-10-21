def build_puml_prompt(diagram_type: str, procedure_text: str, query: str = "") -> str:
    """
    Generates a PlantUML prompt based on UML Selection Schema:
    - Considers query keywords (how, what, why, when)
    - Distinguishes procedural vs. structural content
    - Identifies temporal and component relationships
    """


    query_analysis = ""
    if query:
        query_analysis = (
            f"Analyze the following query to determine UML relevance:\n{query}\n"
            "Focus on:\n"
            "- Keywords (how, what, why, when)\n"
            "- Procedural vs. structural intent\n"
            "- Temporal sequence and component relationships\n\n"
        )
    
    return (
        f"{query_analysis}"
        f"Generate a **{diagram_type}** diagram in PlantUML for the procedure or content below.\n"
        f"Output ONLY PlantUML code starting with @startuml and ending with @enduml.\n"
        f"No explanations, markdown, or comments.\n\n"
        f"Content:\n{procedure_text}"
    )



def build_explanation_prompt(user_type: str, procedure_text: str) -> str:
    """
    Builds a contextually accurate explanation prompt for Gemini
    based on the user's role type and the procedural content.
    """

    if user_type.lower() == "technician":
        role_instr = (
            "You are a certified automotive service technician.\n"
            "Explain this procedure in a clear, technically accurate way.\n"
            "Include detailed workflows, system interactions, and any diagnostic or maintenance steps.\n"
            "Use proper technical terminology and reference possible faults or component relationships when relevant.\n"
            "Your explanation should help a trained technician perform the task safely and efficiently.\n"
            "Focus on step-by-step clarity with diagnostic context when appropriate."
        )
    else:
        role_instr = (
            "You are explaining this to a regular car owner (everyday driver) with no technical background.\n"
            "Provide a simple, easy-to-follow explanation using plain language (around a 6th-grade reading level).\n"
            "Focus on safety tips, everyday usage, and clear step-by-step instructions.\n"
            "Avoid jargon. Use short sentences, friendly tone, and relatable analogies.\n"
            "Summarize the main idea in 1-2 paragraphs, and format as a quick guide or FAQ-style explanation."
        )

    return f"{role_instr}\n\nProcedure:\n{procedure_text}"

