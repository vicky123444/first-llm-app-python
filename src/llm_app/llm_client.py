from __future__ import annotations

from typing import Any

from openai import APIError, APITimeoutError, AuthenticationError, OpenAI, RateLimitError


class LLMClient:
    def __init__(self, api_key: str, model: str, timeout_seconds: int = 30, client: Any | None = None):
        self.client = client or OpenAI(api_key=api_key, timeout=timeout_seconds)
        self.model = model
        self.timeout_seconds = timeout_seconds

    def ask(self, messages: list[dict[str, str]]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
            )
        except AuthenticationError as exc:
            raise ValueError("Authentication failed: check your OPENAI_API_KEY.") from exc
        except RateLimitError as exc:
            raise RuntimeError("Rate limit exceeded. Please try again later.") from exc
        except APITimeoutError as exc:
            raise TimeoutError("The request timed out. Try again with a shorter prompt or retry later.") from exc
        except APIError as exc:
            raise RuntimeError(f"OpenAI API error: {exc}") from exc

        try:
            return response.choices[0].message.content.strip()
        except (AttributeError, IndexError, TypeError) as exc:
            raise RuntimeError("Unexpected response format received from the LLM API.") from exc
