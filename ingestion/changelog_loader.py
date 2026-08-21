# ingestion/changelog_loader.py

from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

CHROMA_DB_PATH = "./chroma_store"
COLLECTION_NAME = "changelog"

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) <= chunk_size:
            current = f"{current}\n\n{paragraph}".strip()
        else:
            if current:
                chunks.append(current)
            current = paragraph

    if current:
        chunks.append(current)

    return chunks

def load_changelog(filepath: str) -> str:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Changelog not found: {filepath}")
    return path.read_text(encoding="utf-8")

def build_collection(library_name: str, changelog_text: str):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn
    )

    chunks = chunk_text(changelog_text)

    collection.add(
        documents=chunks,
        metadatas=[{"library": library_name} for _ in chunks],
        ids=[f"{library_name}_{i}" for i in range(len(chunks))]
    )
    return collection

def query_changelog(library_name: str, query: str, top_k: int = 5) -> list[str]:
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn
    )

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where={"library": library_name}
    )
    return results["documents"][0] if results["documents"] else []

if __name__ == "__main__":
    text = load_changelog("sample_changelog.txt")
    build_collection("pandas", text)

    hits = query_changelog(
        "pandas",
        "deprecated functions and breaking changes"
    )

    for i, hit in enumerate(hits, 1):
        print(f"\n--- Result {i} ---\n{hit}")