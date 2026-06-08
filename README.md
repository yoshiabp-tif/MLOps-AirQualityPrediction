# Sistem Prediksi Kualitas Udara di Jakarta (AQI)

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

## Deskripsi Proyek

Proyek ini merupakan inisiasi pengembangan sistem **Machine Learning Operations (MLOps)** untuk memonitor dan memprediksi kualitas udara di **Kota Jakarta**. Sistem ini dirancang untuk memanfaatkan data kualitas udara yang terus diperbarui secara berkala dan menghasilkan prediksi **Air Quality Index (AQI)** untuk periode waktu mendatang.

Dalam implementasinya, sistem akan menggunakan pendekatan **time-series machine learning** dengan model seperti **XGBoost** untuk memprediksi kondisi kualitas udara **1 jam ke depan** berdasarkan data suhu dan kelembapan saat ini. Selain itu, proyek ini juga dirancang dengan konsep **continuous training**, sehingga model dapat diperbarui secara otomatis ketika terjadi perubahan distribusi data (data drift).

Sumber data kualitas udara diperoleh secara *real-time* dari API penyedia data terbuka yaitu IQAir sumber: https://www.iqair.com/air-quality-monitors/api.

Proyek ini dikembangkan sebagai bagian dari tugas mata kuliah **Machine Learning Operations (MLOps)** dengan tujuan membangun *pipeline machine learning* *end-to-end* yang siap digunakan dalam lingkungan produksi.

---

## Tujuan Proyek

Tujuan utama dari proyek ini adalah:

1. Membangun sistem monitoring kualitas udara berbasis data yang diperbarui secara berkala.
2. Mengembangkan model machine learning untuk memprediksi nilai **AQI (Air Quality Index)** satu jam ke depan.
3. Mengimplementasikan *pipeline* MLOps yang mencakup pengambilan data otomatis, pemrosesan data, pelatihan model (*tracking*), pengujian otomatis (CI/CD), hingga *deployment* model via REST API.
4. Menerapkan konsep **continuous training** agar model tetap relevan terhadap perubahan data lingkungan.

---

## Teknologi yang Digunakan

Beberapa teknologi inti yang digunakan dalam proyek ini antara lain:

* **Bahasa & Algoritma:** Python, XGBoost
* **Manajemen Data:** DVC (Data Version Control)
* **Pelacakan Eksperimen:** MLflow (Tracking & Model Registry)
* **Pengujian & CI/CD:** Pytest, GitHub Actions
* **Infrastruktur & Orkestrasi:** Docker Compose, PostgreSQL
* **Lingkungan Pengembangan:** GitHub Codespaces, Cookiecutter Data Science Template

---

## Struktur Direktori Proyek

Proyek ini menggunakan struktur standar **Cookiecutter Data Science** untuk menjaga organisasi kode tetap rapi dan mudah dikembangkan.
```text
├── .dvc                    <- Konfigurasi internal Data Version Control (DVC)
│   ├── .gitignore
│   └── config
├── .github/workflows       <- Konfigurasi pipeline CI/CD (GitHub Actions)
│   └── mlops-automation.yaml
├── .vscode                 <- Pengaturan environment editor
│   └── settings.json
├── data                    <- Folder utama penyimpanan data
│   ├── external            <- Data dari sumber pihak ketiga
│   ├── processed           <- Dataset final siap pakai
│   ├── .gitignore
│   ├── interim.dvc         <- Tracker DVC untuk data sementara
│   └── raw.dvc             <- Tracker DVC untuk data mentah
├── docs                    <- Dokumentasi proyek (MkDocs)
│   ├── docs/getting-started.md
│   ├── docs/index.md
│   ├── README.md
│   └── mkdocs.yml
├── mlruns/1/models         <- Artefak model & eksperimen yang direkam MLflow
├── models                  <- Folder alternatif model machine learning
├── notebooks               <- Jupyter Notebook untuk eksperimen awal
├── prometheus              <- Konfigurasi Observability (Baru)
│   └── prometheus.yml      <- Konfigurasi scraping metrik
├── references              <- Referensi tambahan / kamus data
├── reports                 <- Laporan analisis & visualisasi
│   └── figures
├── src                     <- Source code utama proyek
│   ├── modeling
│   │   ├── predict.py      <- Skrip inferensi model
│   │   └── train.py        <- Skrip pelatihan model
│   ├── config.py           <- Konfigurasi variabel proyek
│   ├── dataset.py          <- Skrip pemuatan data
│   ├── features.py         <- Skrip ekstraksi fitur
│   ├── ingest_data.py      <- Skrip pengambilan data dari API
│   ├── plots.py            <- Skrip plotting grafik
│   └── preprocess.py       <- Skrip pembersihan data
├── tests                   <- Skrip pengujian otomatis (pytest)
│   └── test_data.py
├── .dvcignore              <- Daftar file yang tidak dilacak oleh DVC
├── .gitignore              <- Daftar file yang tidak dilacak oleh Git
├── Dockerfile              <- Konfigurasi build image Docker
├── LICENSE                 <- Lisensi proyek (MIT)
├── Makefile                <- Perintah shortcut otomatis
├── README.md               <- Dokumentasi utama proyek (Diupdate)
├── docker-compose.yaml     <- File orkestrasi Docker multi-container (Diupdate)
├── mlflow.db               <- Database lokal SQLite untuk Tracking MLflow
├── model_metadata.yaml.dvc <- Tracker DVC untuk metadata model
├── pyproject.toml          <- Konfigurasi metadata proyek Python
├── requirements.txt        <- Daftar dependensi/library Python
└── test_inference.py       <- Skrip manual pengujian inferensi
```
Struktur ini membantu memastikan bahwa seluruh proses pengembangan *data science* dapat dilakukan secara **terstruktur, reproducible, dan scalable**.

---

## Cara Menjalankan Proyek Menggunakan GitHub Codespaces

Proyek ini dikembangkan menggunakan **GitHub Codespaces** untuk memastikan lingkungan pengembangan yang konsisten dan *reproducible*.

### 1. Membuka Codespaces

1. Buka repositori GitHub proyek ini.
2. Klik tombol **Code**.
3. Pilih tab **Codespaces**.
4. Klik **Create Codespace on main**.

GitHub akan secara otomatis membuat lingkungan pengembangan berbasis *cloud*.

### 2. Persiapan Keamanan (API Key)

Untuk dapat menarik data dari IQAir, Anda memerlukan API Key. Buat file bernama `.env` di direktori utama (*root*) proyek dan masukkan kunci Anda:

```env
IQAIR_API_KEY=masukkan_api_key_anda_di_sini

```

### 3. Menjalankan Environment

Setelah Codespaces aktif, *install dependency* proyek dengan:

```bash
pip install -r requirements.txt

```

---

## Arsitektur & Status Proyek (Alur MLOps)

Sistem ini telah terintegrasi dari hulu ke hilir dengan rincian fungsionalitas sebagai berikut:

### 1. Data Ingestion & Preprocessing

* **Pengambilan Data:** Skrip bertugas mengambil data secara *real-time* dari IQAir API dan menyimpannya dalam format mentah `.json` dengan *timestamp* (simulasi periodik).
```bash
python tests/test_iqair_api.py 

```


*(Output data mentah tersimpan di folder `data/raw/`)*
* **Pembersihan Data:** Membaca file JSON, mengekstrak fitur relevan (AQI, Suhu, Kelembapan), menangani duplikasi/nilai kosong, dan merangkumnya menjadi dataset siap pakai (`data/interim/jakarta_aqi_cleaned.csv`).

### 2. Manajemen Versi Data (DVC)

Proyek menggunakan **DVC (Data Version Control)** untuk melacak perubahan dataset kualitas udara tanpa membebani repositori Git. Penyimpanan file data biner diarahkan ke *Remote Storage* terpisah.

**Alur Penambahan Versi Data Baru (Continual Learning):**

1. Tarik data terbaru menggunakan skrip ingestion.
2. Lacak perubahan data dengan DVC: `dvc add data/raw data/interim`.
3. Simpan metadata ke Git: `git add . && git commit -m "update data"`.
4. Dorong data fisik ke remote storage: `dvc push`.
5. Untuk melihat silsilah perubahan: `dvc diff`.

### 3. Pelatihan Model & Registrasi (CI/CD)

Model **XGBoost Regressor** dilatih untuk memprediksi AQI. Seluruh proses pelatihan dilacak otomatis menggunakan **MLflow** untuk mencatat metrik (MAE, RMSE) dan parameter algoritma.
Sistem dilengkapi dengan *pipeline* **GitHub Actions (CI/CD)** yang akan mengevaluasi model secara otomatis. Model hanya akan didaftarkan ke *Model Registry* tahap *Production* jika memenuhi kriteria prinsip *parsimony* (kesederhanaan untuk mencegah *overfitting*) dan lolos ambang batas eror maksimal.

### 4. Orkestrasi Layanan Terintegrasi (Deployment)

Proyek ini menggunakan **Docker Compose** untuk mengorkestrasi Database (PostgreSQL), MLflow Server, dan API Inferensi Model secara bersamaan di dalam satu *bridge network*. Ini memungkinkan model diakses layaknya layanan *real-time* profesional.

Untuk menjalankan seluruh sistem, gunakan perintah:

```bash
docker compose up -d

```

Lalu, untuk mematikan sistem tanpa menghapus data persistensinya:

```bash
docker compose stop

```

## Progres LK-10: Model Serving & Horizontal Scaling
Sistem ini telah ditingkatkan kemampuannya untuk menangani trafik beban tinggi (*high-workload*) menggunakan konsep **Horizontal Scaling** dan **Load Balancing**.
* **Akses Endpoint API:** API Inferensi di-deploy menggunakan image bawaan `mlflow models build-docker` dan dapat diakses melalui Load Balancer Nginx pada `http://localhost:8080/invocations`. Pengujian dapat dilakukan dengan menjalankan `curl -X POST ...`.
* **Cara Menambah Jumlah Replika (Scaling):** Skalabilitas diatur melalui Docker Compose. Untuk menambah jumlah instansi API yang berjalan secara dinamis, ubah nilai `replicas: 3` pada layanan `api-service` di dalam file `docker-compose.yaml`, lalu jalankan kembali perintah `docker compose up -d`. Nginx akan secara otomatis mendistribusikan beban trafik ke seluruh replika yang baru.
---
## Progres LK-11: Implementasi Observability dan Dashboard
Repositori ini memuat arsitektur *Machine Learning Operations* (MLOps) untuk prediksi Kualitas Udara (AQI) di Jakarta menggunakan model berbasis *Machine Learning*. Proyek ini merupakan bagian dari implementasi infrastruktur Capstone Project Kelompok A.3 (Mitra: Epson) di Fakultas Ilmu Komputer (FILKOM), Universitas Brawijaya.

### Arsitektur Microservices
Sistem ini dibangun menggunakan pendekatan *microservices* berbasis Docker, yang terdiri dari komponen berikut:
- **API Service (FastAPI / Uvicorn):** Melayani *request* inferensi model secara *real-time*.
- **Load Balancer (Nginx):** Mengatur distribusi *traffic* dan mengekspos *endpoint* tunggal.
- **Model Registry (MLflow):** Manajemen versi model prediksi secara dinamis.
- **Metrics Scraper (Prometheus):** Mengumpulkan metrik operasional dan *Prediction Drift*.
- **Observability Dashboard (Grafana):** Visualisasi metrik kesehatan sistem secara *real-time*.

### Endpoint & Port Layanan
Setelah kontainer berjalan, layanan dapat diakses melalui:
- **API Inference:** `http://localhost:8080/invocations`
- **Metrik Prometheus (API):** `http://localhost:8080/metrics`
- **MLflow UI:** `http://localhost:5000`
- **Prometheus UI:** `http://localhost:9090`
- **Grafana Dashboard:** `http://localhost:3000`

### Observability & Monitoring (LK-11)
Sistem ini telah dilengkapi dengan instrumen pemantauan (menggunakan `prometheus_client`) untuk melacak:
1. **API Throughput (RPS):** Total jumlah *request* yang diproses.
2. **Inference Latency (P95):** Distribusi waktu respons sistem.
3. **AQI Prediction Distribution (Data Drift):** Deteksi anomali pada sebaran hasil prediksi untuk mengantisipasi penurunan performa model (*Model Decay*).

### Cara Menjalankan Sistem
Pastikan Docker dan Docker Compose telah terinstal.
```bash
# Menjalankan seluruh layanan di background
docker compose up -d

# Mengecek status layanan
docker compose ps

# Mematikan seluruh layanan
docker compose down
```
---

## Dokumentasi Ambang Batas Metrik Pemicu Retraining (LK-12)

Repositori ini menerapkan sistem otomatisasi Continuous Training (CT) berbasis Closed-Loop. Berikut adalah panduan ambang batas metrik yang digunakan sebagai pemicu (trigger) jalurnya latihan ulang otomatis:

| Nama Metrik | Instrumen Pemantau | Ambang Batas (Threshold) | Tindakan Operasional |
| :--- | :--- | :--- | :--- |
| **Prediction Drift** | Evidently AI / Grafana Heatmap | `p-value < 0.05` (Uji KS) | Memicu repositori dispatch untuk menjalankan `train.py` |
| **Model Error** | Prometheus / Grafana Metric | `MAE > 50.0` | Mengaktifkan sinyal peringatan kritis sistem gating |
| **API Load Stabilitas** | Nginx Load Balancer | `Latency P95 > 200ms` | Mengaktifkan algoritma Smart Local Disk Fallback |

### Berkas Konfigurasi Utama:
1. Pipa CI/CD Otomatis: `.github/workflows/mlops-automation.yaml`
2. Tameng Ketahanan API: `src/app.py` (Menggunakan teknik `try-except Local File Store Mount`)
3. Aturan Seleksi Model: `src/modeling/validate.py`

---

**Nama: Yoshia Benedict Parasian**

**NIM: 235150207111012**

**Kelas: MLOps-B**
