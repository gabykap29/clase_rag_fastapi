from infrastructure import VectorStore
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.document_loaders import PyPDFLoader
from schemas import DocumentSchema, RetrieveSchema
from infrastructure import EmbeddingModel


class DocumentService:
    def __init__(self) -> None:
        self.vector_store = VectorStore()
        self.embedding = EmbeddingModel.get_model_embedding()
    
    def add_documents(self, data: DocumentSchema):

        splitter = SemanticChunker(
            embeddings= self.embedding
        )
        loader = PyPDFLoader(str(data.path)).load()

        chunks = splitter.split_documents(loader)

        results = self.vector_store.add_documents(collection_name=data.collection_name, docs=chunks)

        return results

    def retrieve(self, data: RetrieveSchema ):
        return self.vector_store.search_documents(collection_name= data.collection_name, query=data.query, k= data.k)

    