from langchain_text_splitters import RecursiveCharacterTextSplitter # to split documents into chunks (pieces with
# text, saves logic of content)


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return splitter.split_documents(documents)