from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

class VectorStoreManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def create_vector_store(self, texts: List[str], persist_dir: str = "chroma_db"):
        """Create and persist Chroma vector store"""
        documents = self.text_splitter.create_documents(texts)
        return Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=persist_dir
        )

    def get_retriever(self, persist_dir: str = "chroma_db", k: int = 5):
        """Retrieve vector store retriever"""
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=self.embeddings
        ).as_retriever(search_kwargs={"k": k})
