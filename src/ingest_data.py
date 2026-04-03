import requests
import json
import os
import logging
from datetime import datetime

# Setup logging untuk mencatat aktivitas skrip (Best Practice MLOps)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ingest_api_data(api_key):
    """
    Fungsi untuk mengambil data dinamis dari IQAir API dan menyimpannya 
    dengan timestamp agar tidak menimpa data lama (Simulasi Periodik).
    """
    url = "http://api.airvisual.com/v2/city"
    params = {
        "city": "Jakarta",
        "state": "Jakarta",
        "country": "Indonesia",
        "key": api_key
    }
    
    logging.info("Memulai proses Data Ingestion dari IQAir API...")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 
        data = response.json()
        
        if data['status'] == 'success':
            # Pastikan folder data/raw/ tersedia
            os.makedirs("data/raw", exist_ok=True)
            
            # Format nama file menggunakan timestamp untuk mencegah overwrite
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"data/raw/jakarta_aqi_{timestamp}.json"
            
            # Simpan file raw JSON
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
                
            logging.info(f"✅ Data berhasil ditarik dan disimpan di: {filepath}")
        else:
            logging.error(f"❌ API merespons dengan status gagal: {data['status']}")
            
    except Exception as e:
        logging.error(f"❌ Terjadi kesalahan saat Ingestion: {e}")

if __name__ == "__main__":
    # Menggunakan API Key milikmu
    MY_API_KEY = "b7494306-68a0-467f-992b-8831c664fc42"
    ingest_api_data(MY_API_KEY)