# 📄 AIR - AI Research Assistant

An AI-powered **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents, ask questions about them, and receive accurate answers based on the uploaded content.

The application also provides **web search as a fallback** when the uploaded documents do not contain enough information to answer the query.

---

## ✨ Features

- 📑 Upload and ingest multiple PDF documents
- 🧠 Semantic document retrieval using vector embeddings
- 🔍 Intelligent question answering from uploaded documents
- 🛡️ AI-powered answer verification
- 🌐 Web search fallback when document context is insufficient
- 🔗 Display web sources used for web-based answers
- 📚 View retrieved document chunks
- 🎯 Adjustable number of retrieved chunks
- 📊 Relevance indicators for retrieved documents
- 🗑️ Clear uploaded documents and vector database
- 💾 Streamlit session state for preserving application state
- ⚡ Interactive and user-friendly Streamlit interface

---

## 🔄 How It Works

1. PDFs are uploaded and converted into text chunks.
2. Chunks are embedded using Sentence Transformers and stored in ChromaDB.
3. User queries are embedded and the most relevant chunks are retrieved.
4. Groq generates an answer using the retrieved context.
5. A verifier checks whether the answer is supported by the documents.
6. If the answer cannot be reliably generated or verified, Tavily web search is used as a fallback.