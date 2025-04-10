import streamlit as st
import chromadb
import cohere
import requests
from sentence_transformers import SentenceTransformer

# Initialize API keys
TMDB_API_KEY = "a7e7001f97b5ebb3d02dec8af572fa6c"
COHERE_API_KEY = "PpdxkT17wqoBZdYKVjCHfDD4ilF7hY0V7WL8VBZY"

# Initialize clients
chroma_client = chromadb.PersistentClient()
text_collection = chroma_client.get_or_create_collection(name="movie_text")
co = cohere.Client(COHERE_API_KEY)

# Load sentence transformer model
text_model = SentenceTransformer("all-MiniLM-L6-v2")

st.set_page_config(page_title="Movie Chatbot", page_icon="🎬", layout="wide")

# Chatbot UI
st.markdown("<h1 style='text-align: center;'>🎬 Movie Chatbot 🍿</h1>", unsafe_allow_html=True)
st.write("Ask me anything about movies!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Store chat messages

def fetch_tmdb_data(movie_name):
    """Fetch movie details from TMDB"""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(url)
    data = response.json()
    
    if data["results"]:
        movie = data["results"][0]  # Take the first match
        movie_id = movie["id"]
        
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits,images"
        details = requests.get(details_url).json()
        
        return {
            "title": details["title"],
            "description": details["overview"],
            "cast": ", ".join([actor["name"] for actor in details["credits"]["cast"][:5]]),
            "crew": ", ".join([crew["name"] for crew in details["credits"]["crew"][:5]]),
            "image": f"https://image.tmdb.org/t/p/w500{details['poster_path']}" if details.get("poster_path") else None
        }
    return None

def semantic_search(query):
    """Search for a movie in ChromaDB"""
    query_embedding = text_model.encode(query).tolist()
    results = text_collection.query(query_embeddings=[query_embedding], n_results=1)
    
    if results["documents"]:
        return results["metadatas"][0]  # Return metadata from ChromaDB
    return None

def store_in_chromadb(movie_data):
    """Store movie data in ChromaDB."""
    text = f"Title: {movie_data['title']}\nDescription: {movie_data['description']}\nCast: {movie_data['cast']}\nCrew: {movie_data['crew']}"
    embedding = text_model.encode(text).tolist()
    
    text_collection.add(
        ids=[movie_data["title"]],
        documents=[text],
        embeddings=[embedding],
        metadatas=[{
            "title": movie_data["title"],
            "description": movie_data["description"],
            "cast": movie_data["cast"],
            "crew": movie_data["crew"]
        }]
    )
def is_movie_related_llm(query):
    movie_keywords = ["movie", "film", "director", "actor", "cast", "plot", "storyline", "IMDB", "TMDB", "cinema", "box office"]
    return any(keyword in query.lower() for keyword in movie_keywords)


def generate_rag_response(query):
    if not is_movie_related_llm(query):
        return "I can only answer movie-related questions. Please ask something about movies!"
    
    result = semantic_search(query)  # Search ChromaDB

    if not result:  # If not found, fetch from TMDB
        movie_name = query.split("about")[-1].strip()

        movie_data = fetch_tmdb_data(movie_name)

        if movie_data:
            response = co.generate(
                model="command-r-plus",
                prompt=f"Based on the following movie information, answer the query: {query}\n\n{movie_data}",
                max_tokens=150
            ).generations[0].text.strip()

            store_in_chromadb(movie_data)  # Save movie data
            return response + "\n\nWould you like to ask anything else?"
        else:
            return "I couldn't find information on that movie. Would you like me to check something else?"

    response = co.generate(
        model="command-r-plus",
        prompt=f"Based on the following movie information, answer the query: {query}\n\n{result}",
        max_tokens=150
    ).generations[0].text.strip()

    return response + "\n\nWould you like to ask anything else?"

# Chat interface
with st.container():
    for message in st.session_state.chat_history:
        role, text = message
        if role == "user":
            st.markdown(f"<div style='text-align: right; color: white; background: #444; padding: 10px; border-radius: 10px; margin: 5px;'>🤔 {text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; color: black; background: #ddd; padding: 10px; border-radius: 10px; margin: 5px;'>🎬 {text}</div>", unsafe_allow_html=True)

# User input field
user_query = st.text_input("Enter your query:", "")

if st.button("Ask"):
    if user_query:
        response = generate_rag_response(user_query)
        st.session_state.chat_history.append(("user", user_query))
        st.session_state.chat_history.append(("bot", response))
        st.experimental_rerun()  # Refresh to update chat
