"""Hash identifying text before it is written to disk."""

import hashlib


def redact(text: str) -> str:
    """Return a short, stable sha256 digest of ``text``."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
