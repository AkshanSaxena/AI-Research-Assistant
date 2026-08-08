import streamlit as st
import os
from ingest import ingest_documents
from retriever import retrieve_documents
from llm import generate_answer
from llm import generate_web_answer
from verifier import verify_answer
from web_search import web_search

st.set_page_config(
    page_title = "AIR - AI Research Assistant",
    page_icon = "📄",
    layout="wide"
)

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "ingested_files" not in st.session_state:
    st.session_state.ingested_files = False

if "query" not in st.session_state:
    st.session_state.query = ""

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "documents" not in st.session_state:
    st.session_state.documents = []

if "metadatas" not in st.session_state:
    st.session_state.metadatas = []

if "distances" not in st.session_state:
    st.session_state.distances = []

if "context_status" not in st.session_state:
    st.session_state.context_status = ""

if "verdict" not in st.session_state:
    st.session_state.verdict = ""

if "show_web_button" not in st.session_state:
    st.session_state.show_web_button = False

if "web_answer" not in st.session_state:
    st.session_state.web_answer = ""

if "web_sources" not in st.session_state:
    st.session_state.web_sources = []

st.markdown("""
<style>

/* Sidebar */
section[data-testid="stSidebar"]{
    width:290px !important;
    background:#131825 !important;
}

/* Main page width */
.block-container{
    max-width:1350px !important;
    padding-top:2rem !important;
}

/* Main Title */
.main-title{
    font-size:3rem !important;
    font-weight:800 !important;
    text-align:center !important;
    margin-bottom:0 !important;
}

.tag-line{
    text-align:center !important;
    font-size:18px !important;
    color:gray !important;
    margin-top:-10px !important;
    margin-bottom:40px !important;
}

/* Text Area */
textarea{
    font-size:18px !important;
    line-height:1.7 !important;
    padding:20px !important;
    letter-spacing:0.4px;
    border-radius:14px !important;
}

textarea::placeholder{
    font-size:18px !important;
    color:#8b93a6 !important;
}

/* Entire button */
div.stButton > button {
    height: 50px !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
}

/* Text inside the button */
div.stButton > button p {
    font-size: 20px !important;
    font-weight: 600 !important;
}

/* Only tertiary button */
div.stButton > button[kind="tertiary"]{
    position: relative;
    overflow: hidden;
}

div.stButton > button[kind="tertiary"]{
    background: linear-gradient(90deg,#2563eb,#3b82f6);
    border: none !important;
    color: white !important;
    box-shadow:
        0 0 12px rgba(59,130,246,.45),
        0 0 25px rgba(59,130,246,.25);
    transition: all .3s ease;
}

/* Hover */
div.stButton > button[kind="tertiary"]:hover{
    transform: translateY(-2px);
    box-shadow:
        0 0 18px rgba(96,165,250,.7)
}

/* Moving shimmer */
div.stButton > button[kind="tertiary"]::before{
    content:"";
    position:absolute;
    inset:0;
    left:-40%;
    width:40%;
    height:100%;

    background:linear-gradient(
        110deg,
        transparent 0%,
        rgba(255,255,255,.28) 50%,
        transparent 100%
    );

    transform:skewX(-20deg);
    animation: shimmer 3s linear infinite;
}

@keyframes shimmer{
    from{
        left:-50%;
    }
    to{
        left:110%;
    }
}

.answer-box{
    padding:24px !important;
    border-radius:16px !important;
    border:1px solid #2953b5 !important;
    background:#081228 !important;
    box-shadow:0px 0px 18px rgba(41,83,181,0.20) !important;
    font-size:18px !important;
    line-height:1.8 !important;
    text-align:justify !important;
}


/* Expander */
details{
    border-radius:12px !important;
}

.doc-display{
    font-size:16px !important;
    line-height:1.8 !important;
    text-align:justify !important;
}

div[data-testid="stButton"]:has(button[kind="secondary"]) button {
    background-color: #c0392b !important;
    border: 1px solid #c0392b !important;
    color: white !important;
}

div[data-testid="stButton"]:has(button[kind="secondary"]) button:hover {
    background-color: #a93226 !important;
    border: 1px solid #a93226 !important;
}

.footnote1{
    font-size:14px !important;
    letter-spacing:0.3px !important;
    color:gray !important;
}

.footnote2{
    font-size:14px !important;
    letter-spacing:0.3px !important;
    color:gray !important;
    margin-top:-2px !important;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ Settings")

    st.divider()

    st.subheader("📑 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF(s)",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) selected.")

        for file in uploaded_files:
            st.write("📑", file.name)

    if st.button(
        "📥 Ingest Documents",
        use_container_width=True,
        type="primary"
    ):
        if uploaded_files:
            for file in uploaded_files:
                save_path = os.path.join("data", file.name)

                if not os.path.exists(save_path):
                    with open(save_path, "wb") as f:
                        f.write(file.getbuffer())

            with st.spinner("⌛ Generating embeddings..."):
                ingest_documents()

            for file in uploaded_files:
                if file.name not in st.session_state.uploaded_files:
                    st.session_state.uploaded_files.append(file.name)

            st.toast("✅ Documents ingested successfully!")
            st.session_state.ingested_files = True

        else:
            st.warning("Please upload at least one PDF.")

    if st.session_state.ingested_files:
        st.success(f"{len(st.session_state.uploaded_files)} file(s) ingested successfully.")
        
        for name in st.session_state.uploaded_files:
            st.write("📑", name)

    st.divider()

    top_k = st.slider(
        "Retrieved Chunks",
        min_value=1,
        max_value=10,
        value=7
    )
    st.caption("Higher values retrieve more document chunks, increasing context for LLM to generate a response.")

    st.write("")
    show_documents = st.toggle(
        "Show Retrieved Documents",
        value=False
    )

    show_match = st.toggle(
        "Show Relevance Label",
        value=False
    )

    show_sources = st.toggle(
        "Show Sources in case of Web Search",
        value=False
    )

    st.divider()

    st.warning("CAUTION : This clears the retrieved answer.")
    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
        type="secondary"
    ):
        st.session_state.query = ""
        st.session_state.answer = ""
        st.session_state.documents = []
        st.session_state.metadatas = []
        st.session_state.distances = []
        st.session_state.context_status = ""
        st.session_state.verdict = ""
        st.session_state.web_answer = ""
        st.session_state.web_sources = []
        st.session_state.show_web_button = False

        st.toast("🧹 Chat cleared.")
        st.rerun()

    st.divider()

# st.title("📄 AI Research Assistant")
st.markdown(
    """
    <h1 class="main-title">
    📄 AIR - AI Research Assistant
    </h1>
    """,
    unsafe_allow_html=True
)
# st.caption("Ask anything from your documents...")
st.markdown(
    """
    <p class="tag-line">
    Search, Retrieve and Generate intelligently from your documents using AI.
    </p>
    """,
    unsafe_allow_html=True
)

query = st.text_area(
    "Ask something please",
    placeholder="Ask a question from your documents...",
    height=150,
    label_visibility="collapsed"
)

def display_answer(answer):
    st.toast("✅ Answer generated successfully!")
    st.divider()
    st.subheader("✨ Generated Answer :")
    st.markdown(
        f"""
        <div class="answer-box">
            {answer}
        </div>
        """,
        unsafe_allow_html=True
    )

if st.button(
    "🚀 Search & Generate Answer",
    use_container_width=True,
    type="tertiary"
):
    if query.strip():
        st.session_state.query = query
        with st.spinner("🔍 Searching documents..."):
            documents, metadatas, distances = retrieve_documents(query, top_k)

            st.session_state.documents = documents
            st.session_state.metadatas = metadatas
            st.session_state.distances = distances
            
        st.toast(f"📚 Retrieved **{len(documents)}** relevant document chunks.")

        with st.spinner("💭 Generating answer..."):
            result = generate_answer(query, documents)
            answer = result["answer"]
            context_status = result["context_status"]

            # st.session_state.context_status = context_status

        if context_status == "SUFFICIENT":
            with st.spinner("🛡️ Verifying answer..."):
                verification = verify_answer(query, documents, answer)

            verdict = verification["verdict"]

            # st.session_state.verdict = verdict

            if verdict == "SUPPORTED":
                st.session_state.answer = answer

            elif verdict == "PARTIALLY_SUPPORTED":
                st.toast("🛠️ Fine tuning answer...")

                with st.spinner("💭 Re-generating answer..."):
                    result = generate_answer(query, documents)
                    answer = result["answer"]
                    context_status = result["context_status"]

                    # st.session_state.context_status = context_status

                if context_status == "SUFFICIENT":
                    st.session_state.answer = answer

                else:
                    st.warning("The generated answer could not be verified using the uploaded documents.")
                    st.session_state.show_web_button = True
            else:
                st.warning("The generated answer could not be verified using the uploaded documents.")
                st.session_state.show_web_button = True
                
        elif context_status in ["PARTIAL", "INSUFFICIENT"]:
            st.toast("📚 Trying to retrieve more context...")
            new_top_k = min(top_k + 3, 10);

            with st.spinner("🔍 Searching documents..."):
                documents, metadatas, distances = retrieve_documents(query, new_top_k)

                st.session_state.documents = documents
                st.session_state.metadatas = metadatas
                st.session_state.distances = distances

            st.toast(f"📚 Retrieved **{len(documents)}** relevant document chunks.")

            with st.spinner("💭 Re-generating answer..."):
                result = generate_answer(query, documents)
                answer = result["answer"]
                context_status = result["context_status"]

                # st.session_state.context_status = context_status

            if context_status == "SUFFICIENT":
                with st.spinner("🛡️ Verifying answer..."):
                    verification = verify_answer(query, documents, answer)
    
                verdict = verification["verdict"]

                # st.session_state.verdict = verdict

                if verdict in ["SUPPORTED", "PARTIALLY_SUPPORTED"]:
                    st.session_state.answer = answer

                else:
                    st.warning("The generated answer could not be verified using the uploaded documents.")
                    st.session_state.show_web_button = True

            elif context_status in ["PARTIAL", "INSUFFICIENT"]:
                st.warning("The generated answer could not be verified using the uploaded documents.")
                st.session_state.show_web_button = True

if st.session_state.show_web_button:

    if st.button("🌐 Search the Web", 
        use_container_width=True,
        type="primary"
    ):
        st.session_state.show_web_button = False
        with st.spinner("🌐 Searching the web..."):
            web_result = web_search(st.session_state.query)
            answer = web_result["answer"]
            sources = web_result["sources"]

            st.session_state.web_answer = answer
            st.session_state.web_sources = sources

if st.session_state.answer:
    display_answer(st.session_state.answer)

    if show_documents:
        st.divider()
        st.subheader("📚 Retrieved Documents :")
        for doc, meta, distance in zip(
            st.session_state.documents,
            st.session_state.metadatas,
            st.session_state.distances
        ):
            if distance<=0.70:
                score = "🟢 High Relevance"
            elif distance<=0.85:
                score = "🟡 Medium Relevance"
            else:
                score = "🔴 Low Relevance"

            title=(
                f"{meta["source"]} • Page {meta["page"]} • {score}"
                if show_match
                else
                f"{meta["source"]} • Page {meta["page"]}"
            )

            with st.expander(title):
                st.markdown(
                    f"""
                    <div class="doc-display">
                        {doc}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

if st.session_state.web_answer:
    display_answer(st.session_state.web_answer)

    if show_sources:
        st.divider()
        st.subheader("🔗 Sources :")

        for source in st.session_state.web_sources:
            st.markdown(f"• [{source['title']}]({source['url']})")

st.write("")
st.write("")
st.divider()
# st.caption(
#    "Built using **Sentence Transformers**, **ChromaDB**, **Groq LLM**, and **Streamlit**"
# )
# st.caption(
#    "Designed, Developed & Managed by Akshan Saxena."
# )
st.markdown(
    """
    <div class="footnote1">
        <i>Built using <b>Sentence Transformers</b>, <b>ChromaDB</b>, <b>Groq LLM</b>, and <b>Streamlit</b>.</i>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div class="footnote2">
        <i>Designed, Developed & Managed by <b>Akshan Saxena</b>.</i>
    </div>
    """,
    unsafe_allow_html=True
)