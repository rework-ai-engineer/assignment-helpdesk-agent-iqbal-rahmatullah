"""
Modul RAG — mengubah knowledge base menjadi embedding, menyimpannya ke FAISS,
melakukan semantic search, lalu menghasilkan jawaban menggunakan LLM.

Alur ini serupa dengan yang sudah dibangun di Assignment 3 (Semantic Search &
LLM Application) dan Sesi 11 (Building a Simple RAG System) — di assignment ini,
alur tersebut dibungkus menjadi fungsi yang dipanggil oleh router.py.
"""

import os
import pandas as pd
import numpy as np
import faiss
from google import genai  # sesuaikan dengan library Gemini API yang digunakan

_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

KNOWLEDGE_BASE_PATH = "data/it_helpdesk_knowledge_base.csv"

# 🔧 TODO: muat knowledge base dan bangun index FAISS saat aplikasi startup
# (bukan di setiap request), agar lebih efisien. Pertimbangkan menggunakan
# FastAPI startup event atau lazy-loading dengan cache sederhana.

_index = None
_documents = None
_df = None


def _get_embedding(text: str):
    result = _client.models.embed_content(
        model="text-embedding-004",  # sesuaikan versi model embedding
        contents=text,
    )
    return result.embeddings[0].values


def build_index():
    """
    # TODO: implementasikan pembangunan index FAISS dari knowledge base CSV.
    # Referensi: starter_notebook_semantic_search.ipynb dari Assignment 3,
    # Section 1-4 (load data -> unit retrievable -> embedding -> simpan ke FAISS).
    """
    raise NotImplementedError("Implementasikan build_index di sini")


def semantic_search(query: str, top_k: int = 3):
    """
    # TODO: implementasikan semantic search terhadap index yang sudah dibangun.
    # Referensi: starter_notebook_semantic_search.ipynb, Section 5.
    """
    raise NotImplementedError("Implementasikan semantic_search di sini")


async def answer_from_knowledge_base(query: str) -> str:
    """
    Fungsi yang dipanggil router.py ketika intent = 'faq'.
    Menjalankan semantic search, menyusun prompt dengan context hasil retrieval,
    lalu memanggil LLM untuk menghasilkan jawaban.

    # TODO: implementasikan alur lengkap: semantic_search -> build prompt
    # (Persona/Task/Context/Format, lihat Assignment 3 Section 6) -> panggil LLM.
    """
    raise NotImplementedError("Implementasikan answer_from_knowledge_base di sini")
