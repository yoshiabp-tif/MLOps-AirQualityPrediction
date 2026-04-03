import requests
import json
import os
from datetime import datetime

# =====================================================================
# SCRIPT UNTUK BUKTI PENGAMBILAN DATA (LK-03)
# =====================================================================

def fetch_jakarta_aqi(api_key):
    """
    Mengambil data kualitas udara Jakarta dari IQAir API
    """
    # Parameter API untuk Jakarta, Indonesia
    url = "http://api.airvisual.com/v2/city"
    params = {
        "city": "Jakarta",
        "state": "Jakarta",
        "country": "Indonesia",
        "key": api_key
    }
    
    print(f"[{datetime.now()}] Mencoba menghubungi IQAir API...")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Cek apakah ada error HTTP
        
        data = response.json()
        
        if data['status'] == 'success':
            print("\n✅ BERHASIL MENGAMBIL DATA!")
            print("-" * 40)
            
            # Ekstrak data yang relevan sesuai rancangan Skema
            current_data = data['data']['current']
            pollution = current_data['pollution']
            weather = current_data['weather']
            
            print("SKEMA DATA AWAL (Preview):")
            print(f"Timestamp    : {pollution['ts']}")
            print(f"AQI (US)     : {pollution['aqius']}")
            print(f"Main Pollutant: {pollution['mainus']}")
            print(f"Temperature  : {weather['tp']} °C")
            print(f"Humidity     : {weather['hu']} %")
            print("-" * 40)
            
            # Simulasi penyimpanan ke direktori data/raw (Sesuai Cookiecutter)
            # Pastikan folder data/raw ada
            os.makedirs("data/raw", exist_ok=True)
            
            # Format nama file: jakarta_aqi_YYYYMMDD_HHMMSS.json
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/raw/jakarta_aqi_{timestamp_str}.json"
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
                
            print(f"📁 File mentah berhasil disimpan di: {filename}")
            
        else:
            print("❌ Gagal mengambil data. Status:", data['status'])
            
    except requests.exceptions.RequestException as e:
        print("❌ Terjadi kesalahan koneksi:", e)

if __name__ == "__main__":
    # API Key milikmu
    MY_IQAIR_API_KEY = "b7494306-68a0-467f-992b-8831c664fc42" 
    
    # Langsung jalankan fungsinya tanpa perlu pengecekan if lagi
    fetch_jakarta_aqi(MY_IQAIR_API_KEY)