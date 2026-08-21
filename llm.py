import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    api_key = st.secrets["GROQ_API_KEY"]

client = Groq(
    api_key=api_key
)

def generate_answer(query, documents):
    context = ""
    for i, doc in enumerate(documents, start=1):
        context += f"Document {i}:\n{doc}\n\n"


    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        response_format={"type": "json_object"},
        max_completion_tokens=2048,
        temperature=0.4,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document research assistant.\n\n"

                    "Answer ONLY using the retrieved documents.\n"
                    "Do not use outside knowledge.\n"
                    "You may combine information from multiple documents and make simple logical inferences.\n\n"

                    "By default, write a detailed answer of about 200-250 words in 2-3 paragraphs unless the user explicitly asks for a shorter or longer answer.\n\n"

                    "Determine one of these three context statuses:\n"
                    "- SUFFICIENT: The retrieved documents answer the user's query completely. Enough information present in provided documents. \n"
                    "- PARTIAL: Some parts of the query are answered but important information is missing, some parts are not answered properly. \n"
                    "- INSUFFICIENT: The retrieved documents do not contain relevant information. at all for the user asked query. \n\n"

                    "Return ONLY a valid JSON object having EXACTLY these two fields:\n"
                    "- answer (string)\n"
                    "- context_status (SUFFICIENT, PARTIAL or INSUFFICIENT)\n\n"
                    "The value of 'answer' must be a single JSON string."
                    "Do not include markdown."
                    "Do not include code blocks."
                    "Do not include raw newline characters inside the answer string."
                    'Do not return any text outside JSON object. \n'
                    "Do not mention document numbers or document labels in answer. Write answers naturally. \n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Retrieved Documents:\n{context}\n\n"
                    f"Question:\n{query}\n\n"
                )
            }
        ]
    )

    return json.loads(response.choices[0].message.content)

def generate_web_answer(query, web_results):
    context=""
    for i, result in enumerate(web_results, start=1):
        context += (
            f"Source {i}:\n"
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Content: {result['content']}\n\n"
        )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI research assistant. \n"
                    "Answer the user's question only using the provided web search results. \n"
                    "Do not use your own database. \n"
                    "Combine information intelligently from multiple sources when necessary. \n"
                    "If different sources disagree, mention that briefly. \n"
                    "By default, keep the answer around 200-250 words unless the user specifies otherwise. \n"
                    "Do not mention source numbers or URLs in the answer. \n"
                    "If provided context feels insufficient after enough efforts, say it politely. \n"
                    "Give the best framed answer. \n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Web Search Results:\n{context}\n\n"
                    f"Question:\n{query}"
                )
            }
        ]
    )

    return response.choices[0].message.content