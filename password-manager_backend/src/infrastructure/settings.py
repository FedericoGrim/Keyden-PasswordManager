from typing import Optional


def api_docs_enabled(debug: Optional[str]) -> bool:
    """/docs, /redoc and /openapi.json are only exposed in debug."""
    return (debug or "").strip().lower() in {"1", "true", "yes"}
