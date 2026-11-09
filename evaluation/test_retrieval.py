from app.services.retriever import retrieve

query = "How can I identify the final amount paid on a Thai receipt?"

results = retrieve(query, top_k=2)

for result in results:
    print(f"\nSource: {result['source']}")
    print(f"Score: {result['score']:.4f}")
    print(f"Text: {result['text'][:200]}...")