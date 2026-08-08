import os
import fitz
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

def ingest_documents():
    print("Loading vector embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Model ready.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    
    # documents = []

    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(
        name="embedding_info"
    )

    for filename in os.listdir("data"):
        if filename.lower().endswith(".pdf"):
            existing = collection.get(
                where={"source": filename}
            )

            if len(existing["ids"]) > 0:
                print(f"{filename} already ingested. Skipping...")
                continue
            
            pdf_path = os.path.join("data", filename)
            pdf_document = fitz.open(pdf_path)

            # text = ""
            # for page in pdf_document:
            #    text += page.get_text()

            texts = []
            metadatas = []

            for page_num, page in enumerate(pdf_document):
                page_text = page.get_text()

                page_chunks = text_splitter.create_documents([page_text])

                for chunk in page_chunks:
                    texts.append(chunk.page_content)
                    metadatas.append({
                        "source": filename,
                        "page": page_num + 1
                    })

            # documents.append(text)
            pdf_document.close()

            # chunks = text_splitter.create_documents([text])
            # texts = [chunk.page_content for chunk in chunks]
            embeddings = model.encode(texts).tolist()

            file_name = os.path.splitext(filename)[0]
            ids = [f"{file_name}_chunk_{i}" for i in range(len(texts))]
            # metadatas = [{"source": filename} for _ in texts]
            collection.add(
                ids = ids,
                documents = texts,
                embeddings = embeddings,
                metadatas = metadatas
            )

            print(f"Successfully stored {len(texts)} chunks in ChromaDB from {filename}.")
            
if __name__ == "__main__":
    ingest_documents()