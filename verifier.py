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

def verify_answer(query, documents, answer):
    context = ""

    for i, doc in enumerate(documents, start=1):
        context += f"Document {i}:\n{doc}\n\n"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
        max_completion_tokens=1500,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a verifier for a Retrieval-Augmented Generation (RAG) system.\n\n"

                    "Your only task is to determine whether the generated answer is supported by the retrieved documents.\n"
                    "Do not answer the user's question.\n"
                    "Do not use outside knowledge.\n"
                    "Judge only from the retrieved documents.\n\n"

                    "Do not penalize the answer for being concise or omitting details.\n"
                    "Evaluate only the factual claims that are actually made.\n\n"

                    "Return ONLY one valid JSON object containing exactly these fields:\n"
                    "- verdict: SUPPORTED, PARTIALLY_SUPPORTED or NOT_SUPPORTED\n"
                    "- confidence: integer from 0 to 100\n"
                    "- reason: brief explanation in one or two sentences\n\n"

                    "SUPPORTED means every important factual claim is supported.\n"
                    "PARTIALLY_SUPPORTED means most claims are supported but some important claims lack evidence.\n"
                    "NOT_SUPPORTED means major claims are unsupported by the retrieved documents.\n\n"

                    "Do not output anything outside the JSON object."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{query}\n\n"
                    f"Retrieved Documents:\n{context}\n\n"
                    f"Generated Answer:\n{answer}"
                )
            }
        ]
    )

    return json.loads(response.choices[0].message.content)