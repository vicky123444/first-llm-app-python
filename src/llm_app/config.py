from __future__ import annotations

from dataclasses import dataclass
from typing import Final

import os

from dotenv import load_dotenv


DEFAULT_MODEL: Final[str] = "gpt-4o-mini"
DEFAULT_TIMEOUT_SECONDS: Final[int] = 30
PLACEHOLDER_KEY_PREFIXES: Final[tuple[str, ...]] = (
    "your_",
    "demo",
    "example",
    "replace",
    "test-key",
    "fake-",
)


def _is_placeholder_api_key(value: str | None) -> bool:
    if not value:
        return True

    cleaned = value.strip()
    if not cleaned:
        return True

    lowered = cleaned.lower()
    return lowered in {"demo-key", "test-key", "placeholder", "changeme"} or any(
        lowered.startswith(prefix) for prefix in PLACEHOLDER_KEY_PREFIXES
    )


@dataclass(frozen=True)
class Settings:
    api_key: str
    model: str = DEFAULT_MODEL
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if _is_placeholder_api_key(api_key):
            raise ValueError(
                "OPENAI_API_KEY is missing or still set to a placeholder value. "
                "Add a real API key to your .env file or environment."
            )

        model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
        timeout_raw = os.getenv("OPENAI_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS))

        try:
            timeout_seconds = int(timeout_raw)
        except ValueError as exc:
            raise ValueError("OPENAI_TIMEOUT_SECONDS must be an integer.") from exc

        if timeout_seconds <= 0:
            raise ValueError("OPENAI_TIMEOUT_SECONDS must be greater than 0.")

        return cls(api_key=api_key.strip(), model=model, timeout_seconds=timeout_seconds)
