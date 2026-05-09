def unescape(text: str | None) -> str:
    if not text:
        return ""
    return text.replace("\\n", "\n").replace("\\t", "\t")
