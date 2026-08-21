def create_chunks(documents, chunk_size=500, overlap=100):
    """
    Split document text into smaller overlapping chunks.

    Each chunk keeps the original document metadata.
    """

    chunks = []

    for document in documents:

        text = document["text"]
        metadata = document["metadata"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "metadata": metadata.copy()
                })

            # Move forward while keeping some overlap
            start += chunk_size - overlap

    return chunks