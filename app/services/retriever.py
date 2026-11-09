import json
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
INDEX_FILE = BASE_DIR / "evaluation" / "receipt_index.json"


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def retrieve(query, top_k=2):
    index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))

    from app.services.llm import client

    response = client.embeddings.create(
        model="bge-m3",
        input=[query]
    )

    query_embedding = response.data[0].embedding

    results = []

    for chunk in index:
        score = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        results.append({
            "source": chunk["source"],
            "text": chunk["text"],
            "score": score
        })

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:top_k]
