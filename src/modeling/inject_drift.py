import time
import requests
import random

# Endpoint API Load Balancer / Inference Service
URL = "http://localhost:8080/invocations"

def inject_extreme_drift():
    print("🚀 Memulai injeksi data drift ekstrem ke API...")
    print("⚠️ Membanjiri sistem dengan indikator polusi udara tidak wajar (AQI > 350)...")
    
    # Loop untuk mengirimkan 30 request dengan data yang bergeser drastis (Shifted Data)
    for i in range(1, 31):
        # Data normal biasanya berkisar di angka 50-150.
        # Kita injeksi angka acak ekstrem antara 350 hingga 500 untuk merusak distribusi fitur.
        drifted_aqi = random.randint(350, 500)
        drifted_temp = random.randint(42, 50) # Suhu ekstrem fiktif
        
        payload = {
            "dataframe_split": {
                "columns": ["aqi_us", "temperature_c", "humidity_pct"],
                "data": [[drifted_aqi, drifted_temp, 85]]
            }
        }
        
        try:
            response = requests.post(URL, json=payload)
            if response.status_code == 200:
                print(f"[Request #{i}] Berhasil mengirim data drift. Prediksi Model: {response.json()['predictions']}")
            else:
                print(f"[Request #{i}] Gagal. Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error koneksi ke API: {e}")
            
        # Jeda singkat 1 detik antar request agar pergeseran membentuk grafik rapat di Grafana
        time.sleep(1)

if __name__ == "__main__":
    inject_extreme_drift()