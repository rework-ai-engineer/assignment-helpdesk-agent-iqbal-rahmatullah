"""
Modul Tools — fungsi-fungsi "aksi" yang dipanggil router ketika intent
BUKAN pertanyaan informasi/kebijakan, melainkan permintaan spesifik
yang butuh pengecekan data langsung (bukan retrieval semantik).

Pola ini mengikuti konsep Tool Integration di Sesi 12.3.
"""

import pandas as pd

MOCK_TICKETS_PATH = "data/mock_tickets.csv"


def get_ticket_status(ticket_id: str) -> str:
    tid = (ticket_id or "").strip().upper()
  
    tiket = pd.read_csv(MOCK_TICKETS_PATH)
    baris = tiket[tiket["ticket_id"] == tid]
    if baris.empty:
        return f"Tiket {tid or '(kosong)'} tidak ditemukan. Pastikan ID tiket benar (format TICKET-XXXX)."
    r = baris.iloc[0]
    return f"Tiket {tid}: {r.subject}. Status: {r.status}. Update terakhir: {r.last_update}."
