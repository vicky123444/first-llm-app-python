from __future__ import annotations

from typing import Sequence


SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Answer clearly and concisely, "
    "and ask follow-up questions when helpful."
)


def build_user_prompt(question: str) -> str:
    """Return a sanitized user prompt for the model."""
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")
    return question.strip()


def build_messages(history: Sequence[tuple[str, str]] | None = None, question: str | None = None) -> list[dict[str, str]]:
    """Construct a minimal conversation for an LLM request."""
    messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        for role, content in history:
            if role not in {"user", "assistant"}:
                raise ValueError(f"Unsupported role in conversation history: {role}")
            messages.append({"role": role, "content": content})

    if question is not None:
        messages.append({"role": "user", "content": build_user_prompt(question)})

    return messages
