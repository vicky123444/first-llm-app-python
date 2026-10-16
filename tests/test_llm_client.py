from unittest.mock import MagicMock

import pytest
from openai import AuthenticationError

from llm_app.llm_client import LLMClient


@pytest.fixture
def client():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="This is the answer."))]
    )
    return LLMClient(api_key="test-key", model="gpt-4o-mini", timeout_seconds=30, client=mock_client)


def test_ask_returns_message_content(client):
    result = client.ask([{"role": "user", "content": "What is Python?"}])

    assert result == "This is the answer."


def test_ask_handles_auth_error():
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = AuthenticationError(
        "auth failure",
        response=MagicMock(),
        body={},
    )
    client = LLMClient(api_key="test-key", model="gpt-4o-mini", timeout_seconds=30, client=mock_client)

    with pytest.raises(ValueError):
        client.ask([{"role": "user", "content": "hello"}])
