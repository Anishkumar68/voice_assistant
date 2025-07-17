from src.voice_handler import listen, speak
from src.vector_db import vector_db_retrieval as vector_retrieval
from src.llm_handler import query_llm
import time

# from src.speak import speak


def main():
    print("🎙️ Voice Assistant is running... Say something!")
    # speak(text="Hello! I am ready to assist you.")

    while True:
        user_query = input("🗣️ You: ")  # Simulated user input for testing

        # user_query = "what is your name? how can you help me?"  # Simulated user input for testing

        if not user_query:
            continue

        if "exit" in user_query.lower():
            print("👋 Exiting. Goodbye!")
            break

        print(f"🧠 You said: {user_query}")

        # Step 1: Retrieve relevant custom data
        retrieved_chunks = vector_retrieval(query=user_query)
        documents = (
            retrieved_chunks["documents"][0] if "documents" in retrieved_chunks else []
        )

        # Step 2: Build context for LLM
        context = "\n\n".join(documents)
        full_prompt = f"""
You are a robot named Chitti. 
- For general knowledge questions, you can answer based on your training data.
- For specific questions, use the provided context below.

Context:
{context}

Question:
{user_query}
"""

        # Step 3: Query LLM
        response = query_llm(full_prompt)

        print(f"🤖 Chitti: {response}")

        # Step 4: Speak the response
        speak(response)

        # Optional pause before next recording
        time.sleep(1)


if __name__ == "__main__":
    main()
