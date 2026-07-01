import faiss
import numpy as np

index = None
stored_chunks = []


def create_faiss_index(embeddings, chunks):

    global index
    global stored_chunks

    stored_chunks = chunks

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    print(f"FAISS Index Created with {len(chunks)} chunks")

    return index


def search_chunks(query_embedding, top_k=5):

    global index
    global stored_chunks

    if index is None:
        return []

    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    print("\n========== RETRIEVED CHUNKS ==========\n")

    for rank, (score, idx) in enumerate(zip(distances[0], indices[0]), start=1):

        if 0 <= idx < len(stored_chunks):

            print(f"Rank : {rank}")
            print(f"Chunk ID : {idx + 1}")
            print(f"Similarity Score : {score:.4f}")
            print(stored_chunks[idx][:200])
            print("-" * 60)

            results.append({

                "chunk_id": idx + 1,

                "similarity": float(score),

                "text": stored_chunks[idx]

            })

    return results