def build_puml_prompt(diagram_type: str, procedure_text: str) -> str:
    return (
        f"Generate a **{diagram_type}** diagram in PlantUML for this procedure.\n"
        f"Output ONLY PlantUML code starting with @startuml and ending with @enduml.\n"
        f"No explanations, markdown, or comments.\n\n"
        f"Procedure:\n{procedure_text}"
    )


def build_explanation_prompt(user_type: str, procedure_text: str) -> str:
    if user_type.lower() == "technician":
        role_instr = (
            "Explain this procedure concisely with technical detail for a technician. "
            "Focus on key steps and considerations."
        )
    else:
        role_instr = (
            "Explain this procedure briefly in simple terms for a car owner. "
            "Provide a quick, clear overview."
        )

    return f"{role_instr}\n\nProcedure:\n{procedure_text}"