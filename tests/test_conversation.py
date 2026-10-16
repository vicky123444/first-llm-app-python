import pytest

from llm_app.conversation import ConversationHistory


def test_conversation_add_turn_keeps_latest_entries():
    history = ConversationHistory(max_turns=2)
    history.add_turn("Q1", "A1")
    history.add_turn("Q2", "A2")
    history.add_turn("Q3", "A3")

    assert len(history) == 4
    assert history.as_messages()[-2:] == [("user", "Q3"), ("assistant", "A3")]


def test_conversation_rejects_empty_content():
    history = ConversationHistory(max_turns=2)

    with pytest.raises(ValueError):
        history.add_turn("   ", "A1")

    with pytest.raises(ValueError):
        history.add_turn("Q1", "   ")
