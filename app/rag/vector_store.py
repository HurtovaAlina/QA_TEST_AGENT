# takes  chunks + embeddings and saves to Pinecone (service, where vector database is stored).
from pinecone import Pinecone, ServerlessSpec # Pinecone - connects to Pinecone,
# ServerlessSpec - where Pinecone will work
from langchain_pinecone import PineconeVectorStore #(turns langChain documents into Pinecone vector store)

from app.config import pinecone_api_key
from app.rag.embeddings import get_embeddings


def get_vector_store():
    """
        Creates Pinecone vector store.
        :return: connects to Pinecone
        """

    pc = Pinecone(api_key=pinecone_api_key)

    index_name = "qa-test-agent-fdd"  # DB name

    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=3072,  # qty of numbers in vector
            metric="cosine",  # formula for finding similar text
            spec=ServerlessSpec(
                cloud="aws",  # cloud platform amazon
                region="us-east-1"  # region
            ),
        )

    index = pc.Index(index_name) # index for DB

    embeddings = get_embeddings()

    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings
    )

    return vector_store







