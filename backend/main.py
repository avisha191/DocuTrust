from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import interaction_logs
from datetime import datetime

from pypdf import PdfReader

import os

from documents import documents

from services.text_processor import chunk_text
from services.embedding_service import create_embeddings
from services.vector_store import create_faiss_index
from services.llm_service import generate_answer
from services.retriever import retrieve
from services.relevance_grader import grade_retrieval
from services.query_rewriter import rewrite_query
from services.hallucination_checker import check_hallucination

app = FastAPI()

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# CONFIG
# ==========================================================

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

RELEVANCE_THRESHOLD = -2.0

# ==========================================================
# REQUEST MODEL
# ==========================================================

class QuestionRequest(BaseModel):
    question: str

# ==========================================================
# HOME
# ==========================================================

@app.get("/")
def home():
    return {
        "message": "DocuTrust Enterprise CRAG Backend Running 🚀"
    }

# ==========================================================
# UPLOAD PDF
# ==========================================================

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed."
        }

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(file_path)

    extracted_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            extracted_text += text + "\n"

    chunks = chunk_text(extracted_text)

    embeddings = create_embeddings(chunks)

    create_faiss_index(
        embeddings,
        chunks
    )

    document_info = {
        "filename": file.filename,
        "pages": len(reader.pages),
        "chunks": len(chunks),
        "embeddings": len(embeddings),
        "vector_store": "created",
        "preview": extracted_text[:300]
    }

    documents.append(document_info)

    return document_info
# ==========================================================
# DOCUMENTS
# ==========================================================

@app.get("/documents")
def get_documents():
    return documents


# ==========================================================
# SEARCH
# ==========================================================

@app.get("/search")
def search_document(query: str):

    chunks = retrieve(
        query,
        top_k=10
    )

    return {
        "query": query,
        "results": chunks
    }


# ==========================================================
# ASK
# ==========================================================

@app.post("/ask")
def ask_document(request: QuestionRequest):

    question = request.question

    print("\n===================================================")
    print("QUESTION :", question)
    print("===================================================\n")

    # =====================================================
    # STEP 1 : RETRIEVE DOCUMENT CHUNKS
    # =====================================================

    retrieved_chunks = retrieve(
        question,
        top_k=10
    )

    if not retrieved_chunks:

        return {
            "question": question,
            "answer": "No relevant information found in the uploaded document.",
            "sources": [],
            "relevance_score": 0,
            "confidence": 0,
            "hallucination": False
        }

    # =====================================================
    # STEP 2 : RELEVANCE CHECK
    # =====================================================

    relevance_score, best_chunks = grade_retrieval(
        question,
        retrieved_chunks
    )

    print(f"\nInitial Relevance Score : {relevance_score:.4f}")

    rewritten_query = None

    final_chunks = best_chunks
    final_score = relevance_score

    # =====================================================
    # STEP 3 : QUERY REWRITE (ONLY IF NEEDED)
    # =====================================================

    if relevance_score < RELEVANCE_THRESHOLD:

        print("\nLow relevance detected.")
        print("Rewriting query...\n")

        rewritten_query = rewrite_query(question)

        print("Rewritten Query:")
        print(rewritten_query)

        rewritten_chunks = retrieve(
            rewritten_query,
            top_k=10
        )

        if rewritten_chunks:

            rewritten_score, rewritten_best_chunks = grade_retrieval(
                rewritten_query,
                rewritten_chunks
            )

            print(f"\nNew Relevance Score : {rewritten_score:.4f}")

            if rewritten_score > relevance_score:

                print("\nUsing rewritten query.\n")

                final_chunks = rewritten_best_chunks
                final_score = rewritten_score

            else:

                print("\nKeeping original query.\n")
        # =====================================================
    # STEP 4 : BUILD CONTEXT
    # =====================================================

    context = "\n\n".join(
        chunk["text"]
        for chunk in final_chunks
    )

    print("\n================ CONTEXT ================\n")

    for chunk in final_chunks:

        print(f"\n----- Chunk {chunk['chunk_id']} -----\n")

        print(chunk["text"][:300])

        print(
            f"Similarity : {chunk['similarity']:.4f}"
        )

        print(
            f"Rerank Score : {chunk['rerank_score']:.4f}"
        )

    print("\n=========================================\n")

    # =====================================================
    # STEP 5 : GENERATE ANSWER
    # =====================================================

    answer = generate_answer(
        question,
        context
    )

    # =====================================================
    # STEP 6 : HALLUCINATION CHECK
    # =====================================================

    is_supported = check_hallucination(
        question,
        context,
        answer
    )

    # =====================================================
    # STEP 7 : CONFIDENCE SCORE
    # =====================================================

    confidence = 95 if is_supported else 60

    # =====================================================
    # STEP 8 : SAVE INTERACTION TO MONGODB
    # =====================================================

    interaction_logs.insert_one({

        "question": question,

        "rewritten_query": rewritten_query,

        "answer": answer,

        "confidence": confidence,

        "hallucination": not is_supported,

        "relevance_score": float(final_score),

        "chunks_used": len(final_chunks),

        "source_chunks": [
             int(chunk["chunk_id"])
            for chunk in final_chunks
        ],

        "timestamp": datetime.now()

    })

    # =====================================================
    # STEP 9 : RESPONSE
    # =====================================================

    return {

        "question": question,

        "rewritten_query": rewritten_query,

        # Keep for debugging/logging if needed
        "relevance_score": round(float(final_score), 4),

        "confidence": int(confidence),

        "hallucination": not is_supported,

        "chunks_used": int(len(final_chunks)),

        "source_chunks": [
            int(chunk["chunk_id"])
            for chunk in final_chunks
        ],

        "answer": answer,

        "sources": [

            {

                "chunk": int(chunk["chunk_id"]),

                "similarity": round(
                    float(chunk["similarity"]),
                    4
                ),

                "rerank_score": round(
                    float(chunk["rerank_score"]),
                    4
                ),

                "preview": (
                    chunk["text"][:200] + "..."
                    if len(chunk["text"]) > 200
                    else chunk["text"]
                ),

                "full_text": chunk["text"],

            }

            for chunk in final_chunks

        ]

    }