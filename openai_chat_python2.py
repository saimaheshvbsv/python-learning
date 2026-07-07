import os
from openai import OpenAI


def main():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY or OPENAI_API_KEY before running this script.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Keep a single chat_history list that grows with each turn.
    chat_history = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

    questions = [
        "what is the capital of China",
        "Which continent is it in?",
        "List 2 facts about the city",
    ]

    for user_prompt in questions:
        # Append each new user turn to the existing history.
        chat_history.append({"role": "user", "content": user_prompt})

        response = client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            # model="gpt-5",
            messages=chat_history,
        )

        assistant_reply = response.choices[0].message.content
        # Store the assistant reply so the next question is answered in context.
        chat_history.append({"role": "assistant", "content": assistant_reply})

        print("User:", user_prompt)
        print("Assistant:", assistant_reply)
        print()

    print("Chat history:")
    for entry in chat_history:
        print(f"- {entry['role']}: {entry['content']}")


if __name__ == "__main__":
    main()
