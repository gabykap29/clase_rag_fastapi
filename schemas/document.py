from pydantic import BaseModel, Field
from pathlib import Path

class DocumentSchema(BaseModel): 
    collection_name: str = Field(
        description="Este es el nombre de la collecion"
    )
    path: Path = Field(description="La direccion donde esta el documento")


class RetrieveSchema(BaseModel):
    collection_name: str
    query: str
    k: int = 5