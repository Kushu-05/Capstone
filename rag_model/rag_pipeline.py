from retriever import Retriever
from llm import LLM


class RAGPipeline:

    def __init__(self):

        self.retriever = Retriever()
        self.llm = LLM()

    def ask(self, question, top_k=3):

        # 1. Retrieve relevant chunks
        results = self.retriever.search(
            question,
            top_k=top_k
        )

        # 2. Build context for the LLM
        context_parts = []

        for result in results:

            document = result["document"]
            metadata = document["metadata"]

            context_parts.append(
                f"""
Source: {metadata['source']}
Page: {metadata['page']}

{document['text']}
"""
            )

        context = "\n".join(context_parts)

        # 3. Send retrieved context to LLM
        answer = self.llm.generate(
            question,
            context
        )

        return answer, results