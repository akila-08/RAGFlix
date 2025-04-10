# RAGFlix

# OVERVIEW

This project is a **movie-specific chatbot** that leverages **Retrieval-Augmented Generation (RAG)** to intelligently answer movie-related queries. It integrates **ChromaDB**, **Cohere’s LLMs**, and the **TMDB API** to retrieve structured metadata or fetch real-time movie information, then generates informative responses. The interface is built with **Streamlit**, providing an engaging and interactive Q&A experience.

## Movie Query Chatbot

The chatbot processes natural language movie queries and determines whether the question is related to movie data. It performs a **semantic search** using ChromaDB, and if relevant information is not available locally, it fetches metadata using the TMDB API. This metadata is stored for future queries, and answers are generated using **Cohere’s command-r-plus** model.

It supports:
- **Movie descriptions**
- **Cast and crew questions**
- **Plot and storyline inquiries**
- **Search memory via semantic embedding**
- **RAG-based intelligent responses**

---

# TECHNOLOGIES USED

## Retrieval and Storage
- **ChromaDB**: Vector database to persist and query movie metadata using semantic embeddings.
- **Sentence Transformers (`all-MiniLM-L6-v2`)**: Generates dense semantic embeddings of movie texts.
- **SQLite (via ChromaDB)**: Stores movie documents and embeddings for fast retrieval.

## LLM and Generation
- **Cohere (`command-r-plus`)**: Generates human-like answers to user queries by combining input context with retrieved metadata.

## External Data
- **TMDB API**: Fetches movie metadata such as title, overview, cast, crew, and posters from The Movie Database (TMDB).

## Interface
- **Streamlit**: Powers the web interface for interactive user queries and visual chat-based UX.

---

# OUTPUT

Here are some snapshots of our project outcomes:

![image](https://github.com/user-attachments/assets/68b8c011-abf9-43ad-bed3-e0247914c097)

![Screenshot 2025-03-25 160926](https://github.com/user-attachments/assets/04504246-1a32-45b1-8c07-afd8ddc9fc11)

![Screenshot 2025-03-25 161209](https://github.com/user-attachments/assets/8663c8d2-ca4c-4bd9-9dc0-22f00c37f375)

