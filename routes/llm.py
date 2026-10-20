from fastapi import APIRouter, Form
from services import LLMService
from schemas import LLMSchema

router = APIRouter()
llm_service = LLMService()

@router.post("/response")
def response(
    collection_name: str = Form(...),
    input: str = Form(...)
):
    result = llm_service.response(
        data=LLMSchema(
            query=input,
            collection_name= collection_name
        )
    )
    return result
