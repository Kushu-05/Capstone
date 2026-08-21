from embeddings import EmbeddingModel
from vector_store import FAISSVectorStore


class Retriever:

    def __init__(self, vector_db_path="vector_db"):

        print("Loading vector database...")

        self.vector_store = FAISSVectorStore.load(
            vector_db_path
        )

        print("Loading embedding model...")

        self.embedding_model = EmbeddingModel()

    def search(self, query, top_k=3):

        # Convert the user's question into an embedding
        query_embedding = self.embedding_model.encode(
            [query]
        )

        # Search FAISS
        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        return results