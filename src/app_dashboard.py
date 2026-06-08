import streamlit as st
import requests

# 1. Mengatur Desain Tampilan Aplikasi ala Aplikasi Mobile Cuaca
st.set_page_config(page_title="AQI Jakarta Dashboard", page_icon="🌤️", layout="centered")

st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1 style='color: #1E88E5;'>🌤️ AQI Jakarta Predictor App</h1>
        <p style='color: #666;'>Dashboard Inferensi Real-Time Berbasis MLOps Closed-Loop</p>
    </div>
""", unsafe_allow_html=True)

st.write("Geser parameter indikator cuaca di bawah ini untuk menguji performa prediksi model XGBoost secara instan.")

# 2. Form Komponen Input Slider (Rentang Sesuai Statistik Karakteristik Data Asli)
st.subheader("📊 Input Parameter Sensor:")
aqi_us = st.slider("Nilai Indeks AQI US Saat Ini", min_value=0, max_value=500, value=95)
temperature_c = st.slider("Suhu Udara Lingkungan (dalam °C)", min_value=15, max_value=45, value=29)
humidity_pct = st.slider("Tingkat Kelembaban Udara (dalam %)", min_value=10, max_value=100, value=75)

# 3. Tombol Eksekusi Prediksi Pembacaan Model
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Kirim Data & Hitung Prediksi AQI", use_container_width=True):
    # Payload format JSON DataFrame Split bawaan MLflow
    payload = {
        "dataframe_split": {
            "columns": ["aqi_us", "temperature_c", "humidity_pct"],
            "data": [[aqi_us, temperature_c, humidity_pct]]
        }
    }
    
    with st.spinner("Mengirim data ke kluster Docker & menghitung hasil inferensi..."):
        try:
            # Menembak gerbang pintu utama Load Balancer Nginx di port 8080
            response = requests.post("http://localhost:8080/invocations", json=payload)
            response.raise_for_status()
            
            hasil_json = response.json()
            prediksi_aqi = hasil_json["predictions"][0]
            
            # 4. Tampilkan Hasil Inferensi Beserta Variasi Indikator Warna Interaktif
            st.markdown("---")
            st.markdown("<h3 style='text-align: center;'>🔮 Hasil Prediksi AQI Jam Berikutnya:</h3>", unsafe_allow_html=True)
            
            if prediksi_aqi <= 50:
                st.markdown(f"<div style='background-color: #E8F5E9; padding: 20px; border-radius: 10px; text-align: center;'><h2 style='color: #2E7D32;'>🟢 {prediksi_aqi:.2f}</h2><p style='color: #2E7D32; margin:0;'><b>Kategori: SEHAT (GOOD)</b></p></div>", unsafe_allow_html=True)
            elif prediksi_aqi <= 100:
                st.markdown(f"<div style='background-color: #FFFDE7; padding: 20px; border-radius: 10px; text-align: center;'><h2 style='color: #F57F17;'>🟡 {prediksi_aqi:.2f}</h2><p style='color: #F57F17; margin:0;'><b>Kategori: SEDANG (MODERATE)</b></p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background-color: #FFEBEE; padding: 20px; border-radius: 10px; text-align: center;'><h2 style='color: #C62828;'>🔴 {prediksi_aqi:.2f}</h2><p style='color: #C62828; margin:0;'><b>Kategori: TIDAK SEHAT / BERBAHAYA</b></p></div>", unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"❌ Koneksi Terputus: Gagal mendapatkan respons dari API Service Docker. Pastikan perintah 'docker compose up -d' sudah menyala. Info error: {e}")