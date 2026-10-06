from app.rag.document_loader import load_document, split_into_features
from app.rag.document_splitter import split_documents
from app.rag.vector_store import get_vector_store

if __name__ == "__main__": # run this code only when running ingest_fdd.py to avoid loading file in DB more times

    # Read FDD document
    paragraphs = load_document("data/fdd/BEES_Customer.docx")

    # Split FDD into features
    features = split_into_features(paragraphs)

    print("QTY of features:", len(features))

    # Split features into chunks
    chunks = split_documents(features)

    print("QTY of chunks:", len(chunks))

    # Connect to Pinecone
    vector_store = get_vector_store()

    # Add chunks and embeddings to Pinecone
    vector_store.add_documents(chunks)

    print("FDD was successfully added to Pinecone")