ALLOWED_ACTIONS = {
    "add", "remove", "generate", "place", "build", "create"
}

def validate_intent(text: str):
    if not any(word in text for word in ALLOWED_ACTIONS):
        raise ValueError("Unsupported intent")
