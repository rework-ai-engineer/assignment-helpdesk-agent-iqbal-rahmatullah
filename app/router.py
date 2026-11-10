"""
Router — menentukan apakah query user butuh RAG (informasi/kebijakan)
atau tool call (aksi spesifik, misal cek status tiket).

Pola ini mengikuti workflow router yang sudah dipelajari di Sesi 12.4:
  user input -> intent detection -> jika butuh data -> retrieval (RAG)
                                  -> jika butuh aksi -> tool call
"""

from app.rag import answer_from_knowledge_base
from app.tools import get_ticket_status

# 🔧 TODO: import LLM client di sini (Gemini AI API) untuk melakukan intent detection


async def detect_intent(query: str) -> str:
    """
    Menentukan intent dari query user. Harus mengembalikan salah satu:
      - "faq"           -> pertanyaan informasi/kebijakan, arahkan ke RAG
      - "ticket_status"  -> permintaan cek status tiket, arahkan ke tool call

    # TODO: implementasikan intent detection menggunakan LLM (structured prompt,
    # lihat Sesi 10.1) ATAU pendekatan sederhana berbasis keyword sebagai baseline
    # sebelum beralih ke pendekatan berbasis LLM.
    #
    # Contoh prompt yang bisa dipakai sebagai starting point:
    #
    #   "Klasifikasikan pertanyaan berikut ke dalam salah satu kategori:
    #    'faq' (pertanyaan informasi/kebijakan umum) atau
    #    'ticket_status' (permintaan mengecek status tiket tertentu).
    #    Jawab hanya dengan satu kata.
    #    Pertanyaan: {query}"
    """
    raise NotImplementedError("Implementasikan intent detection di sini")


async def handle_query(query: str) -> dict:
    """
    Fungsi utama yang dipanggil oleh endpoint /ask.
    Menjalankan intent detection, lalu merutekan ke RAG atau tool call yang sesuai.
    """
    intent = await detect_intent(query)

    if intent == "ticket_status":
        # 🔧 TODO: ekstrak ticket_id dari query (misal menggunakan regex
        # atau meminta LLM mengekstrak entitas ticket_id dari kalimat user)
        ticket_id = extract_ticket_id(query)
        data = get_ticket_status(ticket_id)
        return {"status": "success", "intent": "ticket_status", "data": data}

    elif intent == "faq":
        data = await answer_from_knowledge_base(query)
        return {"status": "success", "intent": "faq", "data": data}

    else:
        return {"status": "error", "intent": "unknown", "data": "Maaf, saya tidak memahami permintaan Anda."}


def extract_ticket_id(query: str) -> str:
    """
    # TODO: implementasikan ekstraksi ticket_id dari teks query.
    # Format ticket_id pada mock_tickets.csv adalah 'TICKET-XXXX'.
    """
    raise NotImplementedError("Implementasikan ekstraksi ticket_id di sini")
