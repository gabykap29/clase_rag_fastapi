from pydantic import BaseModel

class LLMSchema(BaseModel):
    query: str 
    collection_name: str
    