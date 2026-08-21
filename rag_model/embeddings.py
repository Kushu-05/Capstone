import os
import requests
from dotenv import load_dotenv

load_dotenv()


class EmbeddingModel:

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

    def encode(self, texts):

        response = requests.post(
            f"{self.gateway_url}/v1/embeddings",
            headers=self.headers,
            json={
                "input": texts
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        embeddings = [
            item["embedding"]
            for item in data["data"]
        ]

        return embeddings