import os
import chromadb

client = chromadb.PersistentClient(path="chroma_db")

def clear_database():
    for file in os.listdir("data"):
        path = os.path.join("data", file)

        if os.path.isfile(path):
            os.remove(path)
            
    try:
        client.delete_collection("embedding_info")
    except:
        pass