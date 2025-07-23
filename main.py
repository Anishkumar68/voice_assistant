from src.voice_handler import listen
from src.vector_db import vector_db_retrieval as vector_retrieval
from src.llm_handler import query_llm
from src.speak import speak as sp
import time

WAKE_WORDS = ["hey polo", "chitti", "ok polo", "polo bot"]


def main():
    sp(text="Hello! I am ready to assist you. Say 'Hey Polo' to begin.")

    while True:
        wake_input = input("🔊 Waiting for wake word... ").strip().lower()

        if any(wake_word in wake_input for wake_word in WAKE_WORDS):
            sp("Yes, how can I help you?")
            user_query = input("🗣️ You: ").strip()

            if not user_query:
                continue

            if "exit" in user_query.lower():
                print("👋 Exiting. Goodbye!")
                break

            print(f"🧠 You said: {user_query}")

            # Step 1: Retrieve relevant custom data
            retrieved_chunks = vector_retrieval(query=user_query)
            documents = retrieved_chunks.get("documents", [[]])[0]

            # Step 2: Build context for LLM
            context = (
                "\n\n".join(documents) if documents else "No relevant context found."
            )

            # Step 3: Build prompt
            full_prompt = f"""
You are Polo Bot — a helpful assistant for Polo Cafe.

Your job is to help customers with their questions based on the context provided below.
- If the answer is not found in the context, respond politely and guide the user to contact Gautam or the Polo Cafe team.
- Be brief, accurate, and friendly.

Context:
{context}

Question:
{user_query}
"""

            # Step 4: Query LLM
            response = query_llm(full_prompt)

            print(f"🤖 Chitti: {response}")

            # Step 5: Speak the response
            sp(response)

            time.sleep(1)
        else:
            print("⚠️ Wake word not detected. Please try again.")


if __name__ == "__main__":
    main()
