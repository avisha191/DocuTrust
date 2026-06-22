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

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    # Inner Product + normalized vectors = cosine similarity
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

    # Normalize query vector
    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if (
            idx >= 0 and
            idx < len(stored_chunks)
        ):
            results.append(
                stored_chunks[idx]
            )

    return results