# to find record in Pinecone
from app.rag.vector_store import get_vector_store

if __name__ == "__main__":

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        "User Registration requires Country, Phone Number or Email, Name, Surname and Password",
        k=10
    )

    for i, result in enumerate(results, start=1):
        print(f"\n--- RESULT {i} ---")
        print("Feature:", result.metadata.get("feature"))
        print("Text:", result.page_content)