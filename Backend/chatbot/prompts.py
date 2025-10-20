def build_puml_prompt(diagram_type: str, procedure_text: str) -> str:
    disclaimer = (
        "This text is for documentation and visualization purposes only. "
        "Do NOT provide operational or repair instructions. "
        "The goal is to represent the process conceptually for a technical manual."
    )

    return (
        f"You are an expert PlantUML generator.\n"
        f"Generate a valid **{diagram_type}** diagram that visually represents the following procedure conceptually.\n"
        "Output ONLY PlantUML source code (no explanation, no markdown, no comments).\n"
        "The output must begin with `@startuml` and end with `@enduml`.\n\n"
        f"{disclaimer}\n\n---\nProcedure Description:\n{procedure_text}\n---"
    )


def build_explanation_prompt(user_type: str, procedure_text: str) -> str:
    disclaimer = (
        "Note: The following explanation is for documentation and educational purposes only. "
        "Do NOT treat it as mechanical or safety guidance."
    )

    if user_type.lower() == "technician":
        role_instr = (
            "You are an experienced automotive technician. "
            "Explain the following procedure conceptually with technical insight, "
            "without offering real repair instructions. "
        )
    else:
        role_instr = (
            "You are a friendly assistant explaining to a car owner conceptually what this procedure means, "
            "without giving actual operational steps. You are to give a quick guide responding to the user query."
        )

    return f"{role_instr}\n\n{disclaimer}\n\nProcedure:\n{procedure_text}"
