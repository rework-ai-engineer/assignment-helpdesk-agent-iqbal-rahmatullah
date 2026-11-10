"""
Modul RAG — mengubah knowledge base menjadi embedding, menyimpannya ke FAISS,
melakukan semantic search, lalu menghasilkan jawaban menggunakan LLM.

Alur ini serupa dengan yang sudah dibangun di Assignment 3 (Semantic Search &
LLM Application) dan Sesi 11 (Building a Simple RAG System) — di assignment ini,
alur tersebut dibungkus menjadi fungsi yang dipanggil oleh router.py.
"""

import asyncio
import os

import faiss
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

EMBED_MODEL = "gemini-embedding-001"
GEN_MODEL = "gemini-3.5-flash-lite"
DIMENSI = 768

_client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
    http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=3)),
)


class LLMError(Exception):
    pass

KNOWLEDGE_BASE_PATH = "data/it_helpdesk_knowledge_base.csv"

_index = None
_df = None

NOT_FOUND = "Maaf, saya tidak menemukan informasi tersebut di knowledge base. Silakan hubungi tim IT atau HR."
MIN_SCORE = 0.65

PERSONA = "Kamu adalah asisten IT Helpdesk internal perusahaan. Gaya bicaramu ramah, ringkas, dan akurat."


def _embed(texts: list[str], task_type: str) -> np.ndarray:
    resp = _client.models.embed_content(
        model=EMBED_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(task_type=task_type, output_dimensionality=DIMENSI),
    )
    vec = np.array([e.values for e in resp.embeddings], dtype="float32")
    faiss.normalize_L2(vec)
    return vec


def build_index():
    global _index, _df
    df = pd.read_csv(KNOWLEDGE_BASE_PATH)
    teks = (df["category"] + "\nQ: " + df["question"] + "\nA: " + df["answer"]).tolist()
    vec = _embed(teks, "RETRIEVAL_DOCUMENT")
    index = faiss.IndexFlatIP(DIMENSI) 
    index.add(vec)
    _df, _index = df, index


def semantic_search(query: str, top_k: int = 3) -> list[dict]:
    if _index is None:
        build_index()
    skor, baris = _index.search(_embed([query], "RETRIEVAL_QUERY"), top_k)
    hasil = []
    for s, i in zip(skor[0], baris[0]):
        r = _df.iloc[i]
        hasil.append(
            {"faq_id": int(r.faq_id), "category": r.category, "question": r.question,
             "answer": r.answer, "score": float(s)}
        )
    return hasil


def _build_prompt(query: str, hits: list[dict]) -> str:
    context = "\n\n".join(f"[FAQ {h['faq_id']}] {h['question']}\n{h['answer']}" for h in hits)
    return f"""# Task
Jawab pertanyaan karyawan berdasarkan Context di bawah ini, dan hanya dari Context itu.

# Context
{context}

# Format
- Bahasa Indonesia, maksimal 3 kalimat, langsung ke inti.
- Jangan menambah fakta, angka, atau prosedur yang tidak ada di Context.
- Jika Context tidak memuat jawabannya, jawab persis: "{NOT_FOUND}"

# Pertanyaan
{query}"""


async def answer_from_knowledge_base(query: str) -> str:
    try:
        hits = await asyncio.to_thread(semantic_search, query)
        if not hits or hits[0]["score"] < MIN_SCORE:
            return NOT_FOUND
        resp = await _client.aio.models.generate_content(
            model=GEN_MODEL,
            contents=_build_prompt(query, hits),
            config=types.GenerateContentConfig(system_instruction=PERSONA, temperature=0.2),
        )
    except errors.APIError as e:
        raise LLMError(f"Gemini API gagal: {e.code} {e.status}") from e
    if not resp.text:
        raise LLMError("LLM mengembalikan respons kosong")
    return resp.text.strip()
