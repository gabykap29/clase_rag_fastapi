import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services import DocumentService
from schemas import DocumentSchema

router = APIRouter(tags=["Documents"])
document_service = DocumentService()

DOCUMENT_DIR = Path("documents")
DOCUMENT_DIR.mkdir(exist_ok=True)


@router.post("/add-documents")
def add_document(
    file: UploadFile = File(...),
    collection_name: str = Form(...)
):
    try: 
        path = DOCUMENT_DIR / Path(file.filename).name
        with open(path, "wb") as doc:
            shutil.copyfileobj(file.file, doc)
        results = document_service.add_documents(data= DocumentSchema(
            collection_name=collection_name,
            path=path
        ))
        return results
    except Exception as e:
        raise HTTPException(
            detail=f"Error interno en el servidor {str(e)}",
            status_code = 500
        )
