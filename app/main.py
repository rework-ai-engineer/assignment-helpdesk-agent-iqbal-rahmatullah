"""
Entry point aplikasi FastAPI — IT Helpdesk Assistant.

Alur endpoint utama:
  1. Menerima pertanyaan/permintaan dari user
  2. Meneruskan ke router (router.py) untuk menentukan intent
  3. Router memanggil RAG (rag.py) atau tool (tools.py) sesuai intent
  4. Mengembalikan response terstruktur ke client
"""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from app.rag import LLMError
from app.router import handle_query

logger = logging.getLogger("helpdesk")

app = FastAPI(title="IT Helpdesk Assistant API")


class AskRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    query: str = Field(min_length=1, max_length=500)


class AskResponse(BaseModel):
    status: str
    intent: str
    data: str


def _error(code: int, intent: str, data: str) -> JSONResponse:
    return JSONResponse(status_code=code, content={"status": "error", "intent": intent, "data": data})


@app.exception_handler(RequestValidationError)
async def invalid_request(request: Request, exc: RequestValidationError):
    return _error(422, "unknown", "Request tidak valid: 'query' wajib diisi (1-500 karakter).")


@app.get("/health")
async def health():
    """Endpoint sederhana untuk memastikan service berjalan."""
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    try:
        return AskResponse(**await handle_query(request.query))
    except LLMError:
        logger.exception("LLM gagal merespons")
        return _error(503, "faq", "Layanan AI sedang tidak tersedia. Silakan coba lagi beberapa saat.")
    except Exception:
        logger.exception("Error tak terduga di /ask")
        return _error(500, "unknown", "Terjadi kesalahan internal pada server.")
