# 🔧 TODO: lengkapi Dockerfile berikut mengikuti pola yang sudah dipelajari
# di Sesi 14.2 (FROM python -> WORKDIR -> COPY -> RUN pip -> CMD).

FROM python:3.11-slim

WORKDIR /app

# TODO: copy requirements.txt terlebih dahulu, lalu install dependencies
# (praktik yang baik agar Docker layer caching bekerja optimal)

# TODO: copy seluruh source code aplikasi ke dalam container

# TODO: tentukan port yang akan digunakan (misal 8000) dan expose port tersebut

# TODO: tentukan CMD untuk menjalankan aplikasi FastAPI menggunakan uvicorn
