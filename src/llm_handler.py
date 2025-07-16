from openai import OpenAI as openai
from dotenv import load_dotenv

load_dotenv()

import os

client = openai(
    api_key=os.environ["OPENAI_API_KEY"],  # this is also the default, it can be omitted
)


from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Optional if using .env


def query_llm(prompt: str, model="gpt-4o", temperature=0.4, max_tokens=1000):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that uses provided context to answer questions.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content.strip()
