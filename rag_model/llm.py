import os
import requests
from dotenv import load_dotenv

load_dotenv()


class LLM:

    def __init__(self):

        self.gateway_url = os.getenv("GATEWAY_URL")
        self.learner_key = os.getenv("LEARNER_KEY")

        if not self.gateway_url:
            raise ValueError("GATEWAY_URL is not set")

        if not self.learner_key:
            raise ValueError("LEARNER_KEY is not set")

        self.headers = {
            "Authorization": f"Bearer {self.learner_key}",
            "Content-Type": "application/json",
        }

    def generate(self, question, context):

        system_message = """
You are a helpful company policy assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not invent information.
2. If the answer is not present in the context, say:
   "I could not find that information in the provided documents."
3. Give a concise, clear answer.
4. Use the source information provided in the context.
"""

        user_message = f"""
Context:

{context}

Question:

{question}
"""

        response = requests.post(
            f"{self.gateway_url}/v1/chat/completions",
            headers=self.headers,
            json={
                "messages": [
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]