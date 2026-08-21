import faiss
import numpy as np
import pickle
import os


class FAISSVectorStore:

    def __init__(self, dimension):
        self.dimension = dimension

        # Inner Product works well with normalized embeddings
        self.index = faiss.IndexFlatIP(dimension)

        # Store the original chunks/metadata separately
        self.documents = []

    def add(self, embeddings, documents):

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)

        self.documents.extend(documents)

        print(f"Added {len(documents)} chunks to FAISS.")

    def search(self, query_embedding, top_k=5):

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            results.append({
                "score": float(score),
                "document": self.documents[index]
            })

        return results

    def save(self, path="vector_db"):

        os.makedirs(path, exist_ok=True)

        faiss.write_index(
            self.index,
            f"{path}/index.faiss"
        )

        with open(
            f"{path}/documents.pkl",
            "wb"
        ) as f:

            pickle.dump(
                self.documents,
                f
            )

        print(f"Vector database saved to: {path}")

    @classmethod
    def load(cls, path="vector_db"):

        index = faiss.read_index(
            f"{path}/index.faiss"
        )

        with open(
            f"{path}/documents.pkl",
            "rb"
        ) as f:

            documents = pickle.load(f)

        store = cls(index.d)

        store.index = index
        store.documents = documents

        return store