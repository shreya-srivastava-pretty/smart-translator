def generate_guidance(text: str) -> str:
    """Generate a simple interpretation or advice based on the text."""
    if not text or text.lower().strip() == "":
        return "No meaningful text found on signboard."
    
    if "danger" in text.lower():
        return "Warning: This signboard indicates a danger or hazard. Stay safe."
    if "stop" in text.lower():
        return "This signboard instructs you to stop immediately."
    if "parking" in text.lower():
        return "This signboard is related to parking instructions."

    return "General signboard detected. Follow the instructions as written."
