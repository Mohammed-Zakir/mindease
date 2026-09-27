import chromadb

from sentence_transformers import SentenceTransformer


# Embedding Model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Persistent Vector Database
client = chromadb.PersistentClient(
    path="vector_store"
)


collection = client.get_or_create_collection(
    name="mental_health_docs"
)


def add_document(doc_id, text):

    embedding = embedding_model.encode(text).tolist()

    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding]
    )


def retrieve_context(query, n_results=3):

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results["documents"][0]

def collection_has_data():

    data = collection.get()

    return len(data["ids"]) > 0