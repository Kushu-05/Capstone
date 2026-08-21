from rag_pipeline import RAGPipeline


def main():

    rag = RAGPipeline()

    print("\n==============================")
    print("MULTI-PDF RAG CHAT")
    print("==============================")

    print("\nType 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        if not question.strip():
            continue

        try:

            answer, results = rag.ask(
                question,
                top_k=3
            )

            print("\nAssistant:")
            print(answer)

            print("\nSources:")

            # Remove duplicate sources
            seen = set()

            for result in results:

                metadata = result["document"]["metadata"]

                source = (
                    metadata["source"],
                    metadata["page"]
                )

                if source not in seen:

                    print(
                        f"- {metadata['source']} "
                        f"(Page {metadata['page']})"
                    )

                    seen.add(source)

            print()

        except Exception as e:

            print("\nERROR:")
            print(e)
            print()


if __name__ == "__main__":
    main()