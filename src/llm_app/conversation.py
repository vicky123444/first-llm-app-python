from __future__ import annotations

from collections import deque
from typing import Deque, Iterable, List, Tuple


class ConversationHistory:
    """Store a bounded chat history for a user session."""

    def __init__(self, max_turns: int = 6):
        if max_turns <= 0:
            raise ValueError("max_turns must be a positive integer")
        self.max_turns = max_turns
        self._history: Deque[Tuple[str, str]] = deque(maxlen=max_turns * 2)

    def add_turn(self, user_message: str, assistant_message: str) -> None:
        if not user_message.strip():
            raise ValueError("User message cannot be empty")
        if not assistant_message.strip():
            raise ValueError("Assistant message cannot be empty")

        self._history.append(("user", user_message.strip()))
        self._history.append(("assistant", assistant_message.strip()))

    def as_messages(self) -> List[Tuple[str, str]]:
        return list(self._history)

    def __iter__(self):
        return iter(self._history)

    def __len__(self) -> int:
        return len(self._history)

    def clear(self) -> None:
        self._history.clear()

    @classmethod
    def from_history(cls, history: Iterable[Tuple[str, str]], max_turns: int = 6) -> "ConversationHistory":
        conversation = cls(max_turns=max_turns)
        for role, content in history:
            if role == "user":
                conversation._history.append((role, content))
            elif role == "assistant":
                conversation._history.append((role, content))
            else:
                raise ValueError(f"Unsupported role in conversation history: {role}")
        return conversation
