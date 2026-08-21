from pdf_loader import load_all_pdfs
from chunker import create_chunks
from embeddings import EmbeddingModel
from vector_store import FAISSVectorStore


def main():

    print("\n==============================")
    print("MULTI-PDF RAG")
    print("==============================\n")

    documents = load_all_pdfs("data")

    print(f"\nLoaded {len(documents)} documents.")

    chunks = create_chunks(documents)

    print(f"Created {len(chunks)} chunks.")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print("\nCreating gateway embeddings...")

    embedding_model = EmbeddingModel()

    embeddings = embedding_model.encode(texts)

    print(
        f"Embedding shape: "
        f"({len(embeddings)}, {len(embeddings[0])})"
    )

    dimension = len(embeddings[0])

    vector_store = FAISSVectorStore(
        dimension
    )

    vector_store.add(
        embeddings,
        chunks
    )

    vector_store.save(
        "vector_db"
    )

    print("\n==============================")
    print("VECTOR DATABASE CREATED")
    print("==============================\n")


if __name__ == "__main__":
    main()