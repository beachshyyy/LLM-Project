import json
from pathlib import Path

from app.services.llm import client

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge" / "receipt_guide.md"
INDEX_FILE = BASE_DIR / "evaluation" / "receipt_index.json"

def split_into_chunks(text):
    sections = text.split("\n## ")
    chunks = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        lines = section.splitlines()
        title = lines[0].strip().lstrip("#").strip()
        content = "\n".join(lines[1:]).strip()

        if content:
            chunks.append({
                "source": title,
                "text": content
            })

    return chunks


def main():
    text = KNOWLEDGE_FILE.read_text(encoding="utf-8")
    chunks = split_into_chunks(text)

    print(f"Found {len(chunks)} chunks.")

    response = client.embeddings.create(
        model="bge-m3",
        input=[chunk["text"] for chunk in chunks]
    )

    index = []

    for chunk, embedding_data in zip(chunks, response.data):
        index.append({
            "source": chunk["source"],
            "text": chunk["text"],
            "embedding": embedding_data.embedding
        })

    INDEX_FILE.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Index created: {INDEX_FILE}")
    print(f"Total indexed chunks: {len(index)}")


if __name__ == "__main__":
    main()
