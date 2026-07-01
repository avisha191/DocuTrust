from sentence_transformers import CrossEncoder

# Load CrossEncoder model only once
grader = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def grade_retrieval(question, chunks):
    """
    Reranks retrieved chunks using CrossEncoder.

    Returns:
        best_score (float)
        best_chunks (Top 5 ranked chunks with metadata)
    """

    if not chunks:
        return 0.0, []

    # Create (question, chunk_text) pairs
    pairs = [
        [question, chunk["text"]]
        for chunk in chunks
    ]

    # Predict relevance scores
    scores = grader.predict(pairs)

    # Attach rerank score to each chunk
    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)

    # Sort by rerank score
    ranked_chunks = sorted(
        chunks,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    print("\n========== RERANKED CHUNKS ==========\n")

    for i, chunk in enumerate(ranked_chunks, start=1):

        print(f"Rank : {i}")
        print(f"Chunk ID : {chunk['chunk_id']}")
        print(f"Similarity : {chunk['similarity']:.4f}")
        print(f"Rerank Score : {chunk['rerank_score']:.4f}")
        print(chunk["text"][:200])
        print("-" * 60)

    best_score = ranked_chunks[0]["rerank_score"]

    # Keep top 5 chunks
    best_chunks = ranked_chunks[:5]

    return best_score, best_chunks