from langchain_ollama import OllamaEmbeddings

class EmbeddingModel:
    def __init__(self) -> None:
        pass

    def get_model_embedding() -> OllamaEmbeddings:
        return OllamaEmbeddings(
            model="nomic-embed-text"
        )