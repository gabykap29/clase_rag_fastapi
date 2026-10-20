from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


class VectorStore:
    def __init__(self) -> None:
        self.embedding = OllamaEmbeddings(model="nomic-embed-text")

    def _get_vector_store(self, collection_name) -> Chroma:
        try:
            vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=self.embedding,
                persist_directory="./vector_store",
            )
            return vector_store
        except Exception as e:
            raise e

    def add_documents(self, collection_name: str, docs: list) -> list:
        try:
            vector_store = self._get_vector_store(collection_name=collection_name)
            results = vector_store.add_documents(documents=docs)
            return results
        except Exception as e:
            raise e

    def search_documents(self, collection_name: str, query: str, k: int = 5) -> list:
        try:
            vector_store = self._get_vector_store(collection_name=collection_name)
            results = vector_store.similarity_search(query=query, k=k)
            return results
        except Exception as e:
            raise e
