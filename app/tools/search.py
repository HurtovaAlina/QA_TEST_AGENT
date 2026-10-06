# Request → go to Pinecone → find relevant chunks → return to agent
from langchain_core.documents import Document
from app.rag.vector_store import get_vector_store

def search(query: str) -> list[Document]:
    vector_store = get_vector_store()

    results = vector_store.similarity_search(query, k=4)

    return results

# if __name__ == "__main__":
#     results = search(
#         "What are the password requirements for User Registration?"
#     )
#
#     for result in results:
#         print("\n--- RESULT ---")
#         print("ID:", result.id)
#         print("Feature:", result.metadata.get("feature"))
#         print("Text:", result.page_content)