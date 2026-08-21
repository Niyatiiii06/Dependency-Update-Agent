# search/hybrid_search.py

import chromadb
from rank_bm25 import BM25Okapi
from chromadb.utils import embedding_functions

CHROMA_DB_PATH = "./chroma_store"
COLLECTION_NAME = "changelog"


def hybrid_search(library: str, query: str, top_k: int = 5):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection(
        COLLECTION_NAME,
        embedding_function=embedding_functions.DefaultEmbeddingFunction()
    )

    dense = collection.query(
        query_texts=[query],
        n_results=top_k,
        where={"library": library},
    )["documents"][0]

    data = collection.get(
        where={"library": library},
        include=["documents"],
    )
    documents = data["documents"]

    bm25 = BM25Okapi([doc.lower().split() for doc in documents])
    scores = bm25.get_scores(query.lower().split())
    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True,
    )

    bm25_results = [doc for doc, _ in ranked[:top_k]]

    results = []
    for doc in dense + bm25_results:
        if doc not in results:
            results.append(doc)

    return results[:top_k]


if __name__ == "__main__":
    results = hybrid_search(
        "pandas",
        "deprecated functions and breaking changes",
    )

    for i, result in enumerate(results, 1):
        print(f"\n--- Result {i} ---\n{result}")