# IT Helpdesk Assistant — Starter Repository

Starter repository untuk Assignment 4: End-to-End RAG & AI Agent Development.

## Struktur Project

```
app/
├── main.py       # Entry point FastAPI, berisi endpoint /ask
├── router.py     # Intent detection + routing ke RAG atau tool call
├── rag.py        # Modul RAG: embedding, FAISS, semantic search, LLM answer
└── tools.py      # Modul tool call: pengecekan status tiket

data/
├── it_helpdesk_knowledge_base.csv   # Knowledge base untuk RAG
└── mock_tickets.csv                 # Data mock untuk tool call
```

## TODO Peserta

Seluruh bagian yang perlu diimplementasikan ditandai dengan komentar `# TODO`
atau `# 🔧 TODO` di dalam masing-masing file. Ikuti urutan berikut:

1. `app/rag.py` — implementasikan `build_index()`, `semantic_search()`, `answer_from_knowledge_base()`
2. `app/tools.py` — implementasikan `get_ticket_status()`
3. `app/router.py` — implementasikan `detect_intent()` dan `extract_ticket_id()`
4. `Dockerfile` — lengkapi konfigurasi container

## Menjalankan Secara Lokal (tanpa Docker)

```bash
pip install -r requirements.txt
cp .env.example .env   # lalu isi GEMINI_API_KEY di dalam .env
uvicorn app.main:app --reload
```

## Menjalankan dengan Docker

```bash
docker build -t it-helpdesk-assistant .
docker run -p 8000:8000 --env-file .env it-helpdesk-assistant
```

## Menguji Endpoint

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "berapa jatah cuti tahunan saya?"}'
```

_Lengkapi bagian dokumentasi ini sesuai instruksi pada Assignment Brief (Langkah 10 — Membuat Dokumentasi)._
