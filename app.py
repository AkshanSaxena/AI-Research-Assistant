# from retriever import retrieve_documents
# from llm import generate_answer

# query = input("Ask your question: ")

# documents = retrieve_documents(query)

# answer = generate_answer(query, documents)

# print("\nGroq processed answer: ")
# print(answer)
from web_search import web_search

print(web_search("Who founded the Maratha empire?"))