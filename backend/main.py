from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pypdf import PdfReader

from documents import documents
from services.text_processor import chunk_text
from services.embedding_service import create_embeddings, model
from services.vector_store import create_faiss_index, search_chunks
from services.llm_service import generate_answer

import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "DocuTrust Backend Running 🚀"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed"
        }

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

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


@app.get("/documents")
def get_documents():
    return documents


@app.get("/search")
def search_document(query: str):

    query_embedding = model.encode(query)

    results = search_chunks(
        query_embedding,
        top_k=5
    )

    return {
        "query": query,
        "results": results
    }


@app.post("/ask")
def ask_document(request: QuestionRequest):

    question = request.question

    print("\n=================================")
    print("QUESTION:", question)
    print("=================================")

    query_embedding = model.encode(question)

    relevant_chunks = search_chunks(
        query_embedding,
        top_k=5
    )

    if not relevant_chunks:
        return {
            "question": question,
            "answer": "No relevant information found in the uploaded document.",
            "sources": []
        }

    context = "\n".join(relevant_chunks)

    answer = generate_answer(
        question,
        context
    )

    return {
        "question": question,
        "answer": answer,
        "sources": relevant_chunks
    }