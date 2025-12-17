"""
FastAPI Backend for Physical AI Textbook RAG Chatbot
Integrates with Qdrant for vector search and OpenAI for generation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
import json
import hashlib

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Textbook RAG API",
    description="RAG-powered chatbot for Physical AI and Humanoid Robotics textbook",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "physical_ai_textbook")
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"


class QueryRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None
    conversation_history: Optional[List[dict]] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    context_used: str


class IngestionRequest(BaseModel):
    text: str
    metadata: dict


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Physical AI Textbook RAG API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Check Qdrant connection
        collections = qdrant_client.get_collections()
        qdrant_status = "connected"
    except Exception as e:
        qdrant_status = f"error: {str(e)}"

    return {
        "status": "ok",
        "qdrant": qdrant_status,
        "openai": "configured" if os.getenv("OPENAI_API_KEY") else "not configured"
    }


@app.post("/api/query", response_model=QueryResponse)
async def query_textbook(request: QueryRequest):
    """
    Query the textbook using RAG
    Supports whole-book QA and selected-text QA
    """
    try:
        # Generate embedding for the question
        embedding_response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=request.question
        )
        question_embedding = embedding_response.data[0].embedding

        # Search Qdrant for relevant chunks
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=question_embedding,
            limit=5,
            with_payload=True
        )

        # Extract context from search results
        context_chunks = []
        sources = []

        for result in search_results:
            context_chunks.append(result.payload.get("text", ""))
            sources.append({
                "chapter": result.payload.get("chapter", "Unknown"),
                "section": result.payload.get("section", ""),
                "score": result.score
            })

        context = "\n\n".join(context_chunks)

        # If selected text is provided, prioritize it
        if request.selected_text:
            context = f"SELECTED TEXT:\n{request.selected_text}\n\nADDITIONAL CONTEXT:\n{context}"

        # Build conversation history
        messages = []
        if request.conversation_history:
            messages = request.conversation_history[-6:]  # Keep last 6 messages for context

        # System prompt
        system_prompt = """You are an expert AI tutor for Physical AI and Humanoid Robotics.
Your role is to answer questions based strictly on the textbook content provided.

Guidelines:
- Answer clearly and concisely
- Use examples from the textbook when relevant
- If the question cannot be answered from the provided context, say so
- For technical concepts, explain step-by-step
- If selected text is provided, focus your answer on that specific content first
"""

        messages.insert(0, {"role": "system", "content": system_prompt})
        messages.append({
            "role": "user",
            "content": f"Context from textbook:\n{context}\n\nQuestion: {request.question}"
        })

        # Generate response with OpenAI
        completion = openai_client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )

        answer = completion.choices[0].message.content

        return QueryResponse(
            answer=answer,
            sources=sources,
            context_used=context[:500] + "..." if len(context) > 500 else context
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/api/ingest")
async def ingest_content(request: IngestionRequest):
    """
    Ingest textbook content into Qdrant
    Chunks text and creates embeddings
    """
    try:
        # Generate unique ID for this chunk
        chunk_id = hashlib.md5(request.text.encode()).hexdigest()

        # Generate embedding
        embedding_response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=request.text
        )
        embedding = embedding_response.data[0].embedding

        # Create point for Qdrant
        point = PointStruct(
            id=chunk_id,
            vector=embedding,
            payload={
                "text": request.text,
                **request.metadata
            }
        )

        # Upsert to Qdrant
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point]
        )

        return {
            "status": "success",
            "chunk_id": chunk_id,
            "message": "Content ingested successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting content: {str(e)}")


@app.post("/api/initialize-collection")
async def initialize_collection():
    """
    Initialize Qdrant collection with proper configuration
    """
    try:
        # Check if collection exists
        collections = qdrant_client.get_collections()
        collection_names = [col.name for col in collections.collections]

        if COLLECTION_NAME in collection_names:
            return {
                "status": "exists",
                "message": f"Collection '{COLLECTION_NAME}' already exists"
            }

        # Create collection with text-embedding-3-small dimensions (1536)
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )

        return {
            "status": "created",
            "message": f"Collection '{COLLECTION_NAME}' created successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing collection: {str(e)}")


@app.delete("/api/collection")
async def delete_collection():
    """
    Delete the Qdrant collection (use with caution!)
    """
    try:
        qdrant_client.delete_collection(collection_name=COLLECTION_NAME)
        return {
            "status": "deleted",
            "message": f"Collection '{COLLECTION_NAME}' deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting collection: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
