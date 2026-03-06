# Sistem Prediksi Kualitas Udara Jakarta (AQI)

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

## Deskripsi Proyek

Proyek ini merupakan inisiasi pengembangan sistem **Machine Learning Operations (MLOps)** untuk memonitor dan memprediksi kualitas udara di **Kota Jakarta**. Sistem ini dirancang untuk memanfaatkan data kualitas udara yang terus diperbarui secara berkala dan menghasilkan prediksi **Air Quality Index (AQI)** untuk periode waktu mendatang.

Dalam implementasinya, sistem akan menggunakan pendekatan **time-series machine learning** dengan model seperti **XGBoost** untuk memprediksi kondisi kualitas udara **1 jam ke depan**. Selain itu, proyek ini juga dirancang dengan konsep **continuous training**, sehingga model dapat diperbarui secara otomatis ketika terjadi perubahan distribusi data (data drift).

Sumber data kualitas udara akan diperoleh dari API penyedia data terbuka seperti OpenAQ atau sumber lain yang menyediakan data sensor kualitas udara secara berkala.

Proyek ini dikembangkan sebagai bagian dari tugas mata kuliah **Machine Learning Operations (MLOps)** dengan tujuan membangun pipeline machine learning yang siap digunakan dalam lingkungan produksi.

---

# Tujuan Proyek

Tujuan utama dari proyek ini adalah:

1. Membangun sistem monitoring kualitas udara berbasis data yang diperbarui secara berkala.
2. Mengembangkan model machine learning untuk memprediksi nilai **AQI (Air Quality Index)** satu jam ke depan.
3. Mengimplementasikan pipeline MLOps yang mencakup pengambilan data, pemrosesan data, pelatihan model, hingga deployment model.
4. Menerapkan konsep **continuous training** agar model tetap relevan terhadap perubahan data lingkungan.

---

# Teknologi yang Digunakan

Beberapa teknologi yang akan digunakan dalam proyek ini antara lain:

* Python
* XGBoost
* Jupyter Notebook
* GitHub
* GitHub Codespaces
* Cookiecutter Data Science Template
* MkDocs (dokumentasi proyek)

---

# Struktur Direktori Proyek

Proyek ini menggunakan struktur standar **Cookiecutter Data Science** untuk menjaga organisasi kode tetap rapi dan mudah dikembangkan.

```
├── LICENSE            <- Lisensi proyek (MIT)
├── Makefile           <- Perintah otomatis untuk menjalankan pipeline tertentu
├── README.md          <- Dokumentasi utama proyek
│
├── data
│   ├── external       <- Data dari sumber pihak ketiga (API / dataset eksternal)
│   ├── interim        <- Data hasil transformasi sementara
│   ├── processed      <- Dataset final yang siap digunakan untuk modeling
│   └── raw            <- Data mentah hasil pengambilan dari sumber data
│
├── docs               <- Dokumentasi proyek menggunakan MkDocs
│
├── models             <- Model machine learning yang telah dilatih
│
├── notebooks          <- Notebook untuk eksplorasi data dan eksperimen model
│
├── references         <- Dokumentasi tambahan seperti data dictionary
│
├── reports            <- Laporan analisis atau hasil eksperimen
│   └── figures        <- Visualisasi dan grafik hasil analisis
│
├── requirements.txt   <- Daftar dependency Python
│
├── src                <- Source code utama proyek
│   │
│   ├── config.py      <- Konfigurasi proyek
│   ├── dataset.py     <- Script untuk mengambil atau memuat dataset
│   ├── features.py    <- Feature engineering
│   │
│   ├── modeling
│   │   ├── train.py   <- Script pelatihan model
│   │   └── predict.py <- Script untuk melakukan prediksi
│   │
│   └── plots.py       <- Visualisasi data
```

Struktur ini membantu memastikan bahwa seluruh proses pengembangan data science dapat dilakukan secara **terstruktur, reproducible, dan scalable**.

---

# Cara Menjalankan Proyek Menggunakan GitHub Codespaces

Proyek ini dikembangkan menggunakan **GitHub Codespaces** untuk memastikan lingkungan pengembangan yang konsisten dan reproducible.

### 1. Membuka Codespaces

1. Buka repositori GitHub proyek ini.
2. Klik tombol **Code**.
3. Pilih tab **Codespaces**.
4. Klik **Create Codespace on main**.

GitHub akan secara otomatis membuat lingkungan pengembangan berbasis cloud.

---

### 2. Menjalankan Environment

Setelah Codespaces aktif, terminal dapat digunakan untuk menjalankan perintah Python atau melakukan instalasi dependency.

Install dependency proyek dengan:

```
pip install -r requirements.txt
```

---

### 3. Menjalankan Notebook

Untuk melakukan eksplorasi data atau eksperimen model:

1. Buka folder **notebooks/**
2. Jalankan file **.ipynb** menggunakan Jupyter Notebook yang tersedia di Codespaces.

---

# Branching Strategy

Repositori ini menggunakan **GitHub Flow** sebagai strategi pengelolaan kode.

Alur kerja pengembangan:

1. Branch utama: `main`
2. Setiap fitur atau eksperimen dibuat dalam branch terpisah, misalnya:

```
feat/initial-eda
feat/model-training
feat/api-development
```

3. Setelah fitur selesai dan divalidasi, branch akan digabungkan ke branch `main` melalui **Pull Request**.

Pendekatan ini membantu menjaga stabilitas kode dan memudahkan kolaborasi dalam pengembangan proyek.

---

# Status Proyek

Saat ini proyek masih berada pada tahap **inisiasi dan setup infrastruktur MLOps** yang mencakup:

* Setup repositori GitHub
* Konfigurasi GitHub Codespaces
* Penentuan struktur direktori proyek
* Dokumentasi awal proyek

Tahapan berikutnya akan mencakup:

* Data ingestion dari API kualitas udara
* Eksplorasi data (EDA)
* Pelatihan model prediksi AQI
* Implementasi pipeline machine learning
* Deployment model sebagai API

---

### Nama: Yoshia Benedict Parasian
### NIM: 235150207111012