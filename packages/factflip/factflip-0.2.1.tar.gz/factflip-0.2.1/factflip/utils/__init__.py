def dequote(text: str) -> str:
    if (len(text) >= 2 and text[0] == text[-1]) and text.startswith(("'", '"')):
        return text[1:-1]
    return text
