# Gunakan sistem operasi Python ringan
FROM python:3.10-slim

WORKDIR /app

# Instal seluruh library yang dibutuhkan
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Masukkan seluruh kode sumber
COPY src/ ./src/

# Jalankan server FastAPI menggunakan Uvicorn di port 8080
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]