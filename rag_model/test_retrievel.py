from retriever import Retriever


def main():

    retriever = Retriever()

    questions = [
        "How many annual leave days do employees get?",
        "Do I need approval for purchases above $1000?",
        "Is multi-factor authentication mandatory?",
        "Who should review a contract before signing?"
    ]

    for question in questions:

        print("\n" + "=" * 60)
        print("QUESTION:")
        print(question)
        print("=" * 60)

        results = retriever.search(
            question,
            top_k=3
        )

        for i, result in enumerate(results):

            document = result["document"]
            metadata = document["metadata"]

            print(f"\nRESULT {i + 1}")
            print("-" * 40)

            print(
                f"Score: {result['score']:.4f}"
            )

            print(
                f"Source: {metadata['source']}"
            )

            print(
                f"Page: {metadata['page']}"
            )

            print(
                f"Text:\n{document['text'][:500]}"
            )


if __name__ == "__main__":
    main()