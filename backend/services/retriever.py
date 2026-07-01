from services.embedding_service import model
from services.vector_store import search_chunks


def retrieve(question, top_k=10):

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )[0]

    chunks = search_chunks(
        query_embedding,
        top_k=top_k
    )

    return chunks