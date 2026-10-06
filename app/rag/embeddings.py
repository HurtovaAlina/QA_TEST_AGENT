from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import gemini_api_key


def get_embeddings():

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        api_key=gemini_api_key
    )

    return embeddings