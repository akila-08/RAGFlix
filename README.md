RAGFlix
OVERVIEW
This project is a movie-specific chatbot that leverages RAG (Retrieval-Augmented Generation) using ChromaDB, Cohere’s LLMs, and TMDB API. It intelligently answers movie-related queries by retrieving structured metadata or real-time movie information and generating informative responses through an LLM.
The interface is powered by Streamlit, creating an engaging and interactive movie Q&A experience.

Chatbot Features
The chatbot processes natural language queries about movies, intelligently determines if the query is movie-related, performs semantic search via ChromaDB, and if no data is found, fetches metadata from TMDB, stores it for future queries, and responds using Cohere’s command-r-plus model.

It supports:

Movie descriptions

Cast and crew questions

Plot and storyline inquiries

Search memory via semantic embedding

RAG-based intelligent responses

TECHNOLOGIES USED
Retrieval and Storage
ChromaDB: Vector database to persist and query movie metadata using semantic embeddings.

Sentence Transformers (all-MiniLM-L6-v2): Generates dense semantic embeddings of movie texts.

SQLite (via ChromaDB): Stores movie documents and embeddings for fast retrieval.

LLM and Generation
Cohere (command-r-plus): Generates human-like answers to user queries by combining input context with retrieved metadata.

External Data
TMDB API: Fetches movie metadata such as title, overview, cast, crew, and posters from The Movie Database (TMDB).

Interface
Streamlit: Powers the web interface for interactive user queries and visual chat-based UX.
