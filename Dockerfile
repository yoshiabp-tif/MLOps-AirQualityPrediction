# Menggunakan image Python dasar yang ringan
FROM python:3.10-slim

# Menentukan direktori kerja di dalam kontainer
WORKDIR /app

# Menyalin file requirements.txt dari komputer lokal ke dalam kontainer
COPY requirements.txt .

# Menginstal semua dependensi yang dibutuhkan
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install mlflow==2.10.2 xgboost psycopg2-binary pandas scikit-learn

# Membuka port 8080 agar bisa diakses dari luar
EXPOSE 8080

# Menjalankan server API menggunakan MLflow Model Serving
# Model akan ditarik secara otomatis dari mlflow-server berkat variabel MLFLOW_TRACKING_URI di compose
CMD ["mlflow", "models", "serve", "-m", "models:/AQI_Jakarta_Model/1", "--host", "0.0.0.0", "--port", "8080", "--no-conda"]