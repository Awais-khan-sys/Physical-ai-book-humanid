"""
Script to ingest textbook chapters into Qdrant
Chunks text intelligently and creates embeddings
"""

import os
import sys
import glob
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
import re
import hashlib
from typing import List, Dict

load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "physical_ai_textbook")
EMBEDDING_MODEL = "text-embedding-3-small"


def chunk_markdown_by_sections(markdown_text: str, chapter_name: str) -> List[Dict]:
    """
    Chunk markdown text by sections (## headings)
    Preserves semantic coherence
    """
    chunks = []

    # Split by ## headings (sections)
    sections = re.split(r'\n## ', markdown_text)

    # First section is before any ## heading (includes # title)
    if sections[0].strip():
        # Extract chapter title
        title_match = re.match(r'# (.+)', sections[0])
        title = title_match.group(1) if title_match else chapter_name

        chunks.append({
            "text": sections[0].strip(),
            "chapter": chapter_name,
            "section": "Introduction",
            "title": title
        })

    # Process each section
    for i, section in enumerate(sections[1:], 1):
        # Extract section heading
        lines = section.split('\n', 1)
        section_heading = lines[0].strip()
        section_content = lines[1].strip() if len(lines) > 1 else ""

        full_text = f"## {section_heading}\n\n{section_content}"

        # If section is too long (>2000 chars), split by ### subheadings
        if len(full_text) > 2000:
            subsections = re.split(r'\n### ', section_content)

            # First part (before any ###)
            if subsections[0].strip():
                chunks.append({
                    "text": f"## {section_heading}\n\n{subsections[0].strip()}",
                    "chapter": chapter_name,
                    "section": section_heading,
                    "title": section_heading
                })

            # Process subsections
            for subsection in subsections[1:]:
                sublines = subsection.split('\n', 1)
                subsection_heading = sublines[0].strip()
                subsection_content = sublines[1].strip() if len(sublines) > 1 else ""

                chunks.append({
                    "text": f"### {subsection_heading}\n\n{subsection_content}",
                    "chapter": chapter_name,
                    "section": section_heading,
                    "subsection": subsection_heading,
                    "title": f"{section_heading} - {subsection_heading}"
                })
        else:
            chunks.append({
                "text": full_text,
                "chapter": chapter_name,
                "section": section_heading,
                "title": section_heading
            })

    return chunks


def create_collection():
    """Create Qdrant collection if it doesn't exist"""
    try:
        collections = qdrant_client.get_collections()
        collection_names = [col.name for col in collections.collections]

        if COLLECTION_NAME not in collection_names:
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=1536,  # text-embedding-3-small dimension
                    distance=Distance.COSINE
                )
            )
            print(f"✓ Created collection: {COLLECTION_NAME}")
        else:
            print(f"✓ Collection already exists: {COLLECTION_NAME}")
    except Exception as e:
        print(f"✗ Error creating collection: {e}")
        sys.exit(1)


def ingest_chunks(chunks: List[Dict]):
    """Generate embeddings and ingest chunks into Qdrant"""
    print(f"\n📥 Ingesting {len(chunks)} chunks...")

    points = []
    for i, chunk in enumerate(chunks, 1):
        try:
            # Generate embedding
            embedding_response = openai_client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=chunk["text"]
            )
            embedding = embedding_response.data[0].embedding

            # Create unique ID
            chunk_id = hashlib.md5(chunk["text"].encode()).hexdigest()

            # Create point
            point = PointStruct(
                id=chunk_id,
                vector=embedding,
                payload=chunk
            )
            points.append(point)

            print(f"  [{i}/{len(chunks)}] {chunk['chapter']} - {chunk.get('section', 'N/A')}")

            # Batch upsert every 10 chunks
            if len(points) >= 10:
                qdrant_client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=points
                )
                points = []

        except Exception as e:
            print(f"  ✗ Error processing chunk {i}: {e}")
            continue

    # Upsert remaining points
    if points:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

    print(f"✓ Ingestion complete!")


def main():
    """Main ingestion pipeline"""
    
    print("🚀 Physical AI Textbook Ingestion Pipeline")
    print("=" * 50)

    # Check for docs directory
    docs_dir = "../docs"
    if not os.path.exists(docs_dir):
        docs_dir = "./docs"
    if not os.path.exists(docs_dir):
        print(f"✗ Error: docs directory not found")
        sys.exit(1)

    # Create collection
    create_collection()

    # Find all markdown files
    md_files = glob.glob(os.path.join(docs_dir, "*.md"))
    print(f"\n📚 Found {len(md_files)} markdown files")

    all_chunks = []

    # Process each file
    for md_file in md_files:
        filename = os.path.basename(md_file)
        chapter_name = filename.replace(".md", "").replace("-", " ").title()

        print(f"\n📖 Processing: {filename}")

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        chunks = chunk_markdown_by_sections(content, chapter_name)
        all_chunks.extend(chunks)

        print(f"  ✓ Created {len(chunks)} chunks")

    # Ingest all chunks
    ingest_chunks(all_chunks)

    print("\n" + "=" * 50)
    print(f"✅ Successfully ingested {len(all_chunks)} chunks into Qdrant!")
    print(f"📊 Collection: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()
