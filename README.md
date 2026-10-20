# RAG con FastAPI + Ollama + ChromaDB

API simple de **RAG (Retrieval Augmented Generation)**. Permite subir un PDF, indexarlo en una base vectorial y hacerle preguntas a un LLM local que responde usando solo el contenido del documento.

Todo corre en local: no necesita API keys.

## Cómo funciona

```
 PDF ──► /add-documents ──► PyPDFLoader ──► SemanticChunker ──► embeddings ──► ChromaDB
                                              (nomic-embed-text)               (./vector_store)

 Pregunta ──► /response ──► búsqueda por similitud (top 5) ──► prompt + contexto ──► LLM (Ollama) ──► respuesta
```

1. **Indexación**: el PDF se guarda en `documents/`, se divide en chunks semánticos (`SemanticChunker`) y se guardan sus embeddings en una *colección* de Chroma.
2. **Consulta**: se buscan los 5 chunks más parecidos a la pregunta, se inyectan en el prompt como contexto y el LLM responde. Si el contexto no alcanza, responde `"esta pregunta está fuera de mis limites!"`.

## Requisitos

- Python 3.12
- [Ollama](https://ollama.com) corriendo en local (`http://localhost:11434`)
- Modelos en Ollama:
  - Embeddings: `nomic-embed-text`
  - LLM: `qwen3.5-4b-Q4_K_M` (nombre configurado en `infrastructure/llm.py`)

```bash
ollama pull nomic-embed-text
ollama list   # verificá que el LLM exista con ese nombre exacto
```

> Si tu modelo LLM se llama distinto (o querés usar otro), cambiá `model=` en `infrastructure/llm.py`.

## Instalación

```bash
uv venv env
source env/bin/activate        # en fish: source env/bin/activate.fish 
uv pip install -r requirements.txt

## Ejecutar

Desde la raíz del proyecto (importante: las rutas `documents/` y `vector_store/` son relativas):

```bash
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Docs interactivas (Swagger): http://127.0.0.1:8000/docs

## Endpoints

| Método | Ruta             | Descripción                                   | Body (`multipart/form-data`)          |
|--------|------------------|-----------------------------------------------|---------------------------------------|
| GET    | `/`              | Health check → `{"server": true}`             | —                                     |
| POST   | `/add-documents` | Sube un PDF e indexa sus chunks en Chroma     | `file` (PDF), `collection_name`       |
| POST   | `/response`      | Pregunta al LLM usando el contexto recuperado | `collection_name`, `input`            |

### Ejemplo

1. Indexar un documento en la colección `clase`:

```bash
curl -X POST http://127.0.0.1:8000/add-documents \
  -F "file=@documents/RAG (Retrieval Augmented Generation)-3.pdf" \
  -F "collection_name=clase"
```

Devuelve la lista de IDs de los chunks guardados.

2. Hacer una pregunta:

```bash
curl -X POST http://127.0.0.1:8000/response \
  -F "collection_name=clase" \
  -F "input=¿Qué es RAG?"
```

La `collection_name` de la pregunta debe ser la misma con la que indexaste el documento.

## Estructura del proyecto

```
main.py                  # App FastAPI, registra los routers
routes/
  documents.py           # POST /add-documents
  llm.py                 # POST /response
services/
  documents.py           # DocumentService: chunking + guardado + retrieve
  llm.py                 # LLMService: arma el prompt con contexto y llama al LLM
infrastructure/
  embedding.py           # OllamaEmbeddings (nomic-embed-text)
  llm.py                 # OllamaLLM (temperature=0, sin reasoning)
  vector_store.py        # Wrapper de Chroma (add / similarity_search)
prompts/prompt.py        # Prompt template del asistente
schemas/                 # Modelos Pydantic (DocumentSchema, RetrieveSchema, LLMSchema)
documents/               # PDFs subidos (incluye uno de ejemplo sobre RAG)
vector_store/            # Base de datos Chroma persistida (se crea sola)
```

## Configuración rápida

| Qué                      | Dónde                              |
|--------------------------|------------------------------------|
| Modelo LLM / temperatura | `infrastructure/llm.py`            |
| Modelo de embeddings     | `infrastructure/embedding.py` y `infrastructure/vector_store.py` (están en ambos, cambiá los dos) |
| Cantidad de chunks (`k`) | `schemas/document.py` (`RetrieveSchema.k`, default 5) |
| Prompt                   | `prompts/prompt.py`                |
| Carpeta de la DB         | `infrastructure/vector_store.py` (`persist_directory`) |

## Limitaciones conocidas / ideas para mejorar

- Solo soporta **PDF**.
- Subir el mismo PDF dos veces duplica los chunks en la colección.
- No hay endpoint para listar/borrar colecciones o documentos.
- Los endpoints son síncronos(Lo ideal seria usar siempre async-await, que con fastAPI lo podemos usar de forma nativa ) y el `SemanticChunker` es lento en PDFs grandes (llama al modelo de embeddings por cada oración, pero suele ser mas efectivo que otros documentos).
