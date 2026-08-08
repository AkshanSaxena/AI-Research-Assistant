import chromadb
from sentence_transformers import SentenceTransformer

print("Loading retriever vector embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model ready from retriever.")

def retrieve_documents(query, top_k):
    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_collection(
        name = "embedding_info"
    )

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings = [query_embedding],
        n_results = top_k,
        include = ["documents", "distances", "metadatas"]
    )

    print("\nDistances:")
    print(results["distances"][0])

    print("\nSources:")
    print(results["metadatas"][0])

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    return documents, metadatas, distances

if __name__ == "__main__":
    query = input("Enter your question: ")
    documents = retrieve_documents(query)

    print("\nRetrieved Documents: ")
    for i, doc in enumerate(documents, start=1):
        print(f"\nDocument {i}: ")
        print(doc)
        print("-" * 50)