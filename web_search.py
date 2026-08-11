import streamlit as st
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    api_key = st.secrets["TAVILY_API_KEY"]

client = TavilyClient(
    api_key=api_key
)

def web_search(query):
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=10,
        include_answer=True,
        include_raw_content=True
    )

    sources = []

    for result in response["results"]:
        sources.append({

            "title": result["title"],
            "url": result["url"]
        })

    return {
        "answer": response["answer"],
        "sources": sources
    }