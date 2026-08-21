import os
import fitz


def load_all_pdfs(data_dir):
    """
    Load all PDF files from the data directory.

    Returns:
        list of dictionaries containing:
        - text
        - metadata
    """

    documents = []

    for filename in os.listdir(data_dir):

        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(data_dir, filename)

        print(f"Loading: {filename}")

        pdf = fitz.open(file_path)

        for page_number, page in enumerate(pdf):

            text = page.get_text()

            if not text.strip():
                continue

            documents.append({
                "text": text,
                "metadata": {
                    "source": filename,
                    "page": page_number + 1
                }
            })

        pdf.close()

    return documents