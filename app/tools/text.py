def parse_text(data: bytes) -> str:
    return data.decode("utf-8", errors="ignore").strip()


