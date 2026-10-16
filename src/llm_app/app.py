from __future__ import annotations

from llm_app.config import Settings
from llm_app.conversation import ConversationHistory
from llm_app.llm_client import LLMClient
from llm_app.prompts import build_messages


def run_cli() -> None:
    settings = Settings.from_env()
    client = LLMClient(api_key=settings.api_key, model=settings.model, timeout_seconds=settings.timeout_seconds)
    conversation = ConversationHistory(max_turns=4)

    print("Welcome to the Python LLM Assistant!")
    print()

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            print("\nGoodbye!")
            break

        if user_input.strip().lower() in {"exit", "quit", "bye"}:
            print("Goodbye!")
            break

        try:
            response = client.ask(build_messages(history=conversation.as_messages(), question=user_input))
            print(f"Assistant: {response}")
            conversation.add_turn(user_input, response)
        except (ValueError, RuntimeError, TimeoutError) as exc:
            print(f"Assistant: Error: {exc}")

        print()


if __name__ == "__main__":
    run_cli()
