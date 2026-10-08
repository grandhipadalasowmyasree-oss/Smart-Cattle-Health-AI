from .read_document import read_pdf


# ============================================================
# CREATE SEMANTIC CHUNKS
# ============================================================

def create_chunks(text):

    sections = text.split("\n")

    chunks = []

    current_chunk = ""

    for line in sections:

        line = line.strip()

        if not line:
            continue

        # Start a new chunk when an important section begins
        important_section = (
            line.startswith("3. General")
            or line.startswith("4.")
            or line.startswith("5.")
            or line.startswith("6.")
            or line.startswith("7.")
            or line.startswith("8.")
            or line.startswith("9.")
            or line.startswith("10.")
        )

        if important_section and current_chunk.strip():

            chunks.append(current_chunk.strip())

            current_chunk = ""

        current_chunk += line + "\n"

    # Add final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    text = read_pdf()

    if not text:

        print("❌ No document text found!")

    else:

        chunks = create_chunks(text)

        print("\n✅ Semantic chunking successful!")

        print("Total characters:", len(text))

        print("Total chunks:", len(chunks))

        for i, chunk in enumerate(chunks, start=1):

            print(
                f"\n--- CHUNK {i} ---\n"
            )

            print(chunk[:500])

            print("\n--------------------------------")