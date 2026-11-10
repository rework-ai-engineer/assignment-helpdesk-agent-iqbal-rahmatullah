"""
Router — menentukan apakah query user butuh RAG (informasi/kebijakan)
atau tool call (aksi spesifik, misal cek status tiket).

Pola ini mengikuti workflow router yang sudah dipelajari di Sesi 12.4:
  user input -> intent detection -> jika butuh data -> retrieval (RAG)
                                  -> jika butuh aksi -> tool call
"""

import re

from app.rag import answer_from_knowledge_base
from app.tools import get_ticket_status

_TICKET_ID_RE = re.compile(r"\bTICKET-\d+\b", re.IGNORECASE)

_AKSI_CEK = ("status", "cek", "check", "progress", "perkembangan", "sampai mana")

ASK_TICKET_ID = 'Mohon sebutkan ID tiket Anda (format TICKET-XXXX), misalnya: "Cek status TICKET-0005".'


async def detect_intent(query: str) -> str:
    q = query.lower()
    menyebut_tiket = "tiket" in q or "ticket" in q
    if _TICKET_ID_RE.search(query) or (menyebut_tiket and any(k in q for k in _AKSI_CEK)):
        return "ticket_status"
    return "faq"


def extract_ticket_id(query: str) -> str | None:
    m = _TICKET_ID_RE.search(query)
    return m.group().upper() if m else None


async def handle_query(query: str) -> dict:
    intent = await detect_intent(query)

    if intent == "ticket_status":
        ticket_id = extract_ticket_id(query)
        if ticket_id is None:
            return {"status": "error", "intent": "ticket_status", "data": ASK_TICKET_ID}
        data = get_ticket_status(ticket_id)
        return {"status": "success", "intent": "ticket_status", "data": data}

    elif intent == "faq":
        data = await answer_from_knowledge_base(query)
        return {"status": "success", "intent": "faq", "data": data}

    else:
        return {"status": "error", "intent": "unknown", "data": "Maaf, saya tidak memahami permintaan Anda."}
