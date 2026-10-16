from __future__ import annotations

import pytest

from llm_app.config import Settings
from llm_app.prompts import SYSTEM_PROMPT, build_messages, build_user_prompt


def test_build_user_prompt_rejects_empty_question():
    with pytest.raises(ValueError):
        build_user_prompt("   ")


def test_build_messages_includes_system_and_question():
    messages = build_messages(question="What is Python?")

    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM_PROMPT
    assert messages[-1] == {"role": "user", "content": "What is Python?"}


def test_build_messages_with_history_keeps_order():
    history = [("user", "Hi"), ("assistant", "Hello!")]
    messages = build_messages(history=history, question="How are you?")

    assert messages[1] == {"role": "user", "content": "Hi"}
    assert messages[2] == {"role": "assistant", "content": "Hello!"}
    assert messages[3] == {"role": "user", "content": "How are you?"}


def test_settings_rejects_placeholder_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "demo-key")
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_TIMEOUT_SECONDS", raising=False)

    with pytest.raises(ValueError, match="real API key"):
        Settings.from_env()
