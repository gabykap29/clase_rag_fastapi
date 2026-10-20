from infrastructure import LLMModel
from prompts.prompt import prompt
from services import DocumentService
from schemas import LLMSchema, RetrieveSchema

class LLMService:
    def __init__(self):
        self.llm_model = LLMModel.get_model()
        self.document_service = DocumentService()

    def response(self, data: LLMSchema):
        try: 
            input = prompt.invoke({
                "context": self.document_service.retrieve(
                    RetrieveSchema(
                        collection_name= data.collection_name,
                        query= data.query,
                    )),
                "input_user": data.query
            })

            response = self.llm_model.invoke(input= input)
            return response
        except Exception as e:
            raise e
