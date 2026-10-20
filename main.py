from fastapi import FastAPI
from routes.documents import router
from routes.llm import router as llm_router
app = FastAPI(title="RAG")

@app.get("/")
def root():
    return {
        "server": True
    }

app.include_router(router)
app.include_router(llm_router)