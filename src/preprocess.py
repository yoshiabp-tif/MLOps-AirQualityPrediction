import os
import json
import glob
import logging
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_data():
    """
    Membaca semua file JSON di data/raw/, mengekstrak fitur penting,
    membersihkan data, dan menyimpannya sebagai CSV di data/interim/.
    """
    raw_dir = "data/raw"
    interim_dir = "data/interim"
    
    # Pastikan folder interim ada
    os.makedirs(interim_dir, exist_ok=True)
    
    # Cari semua file JSON hasil ingestion
    json_files = glob.glob(os.path.join(raw_dir, "*.json"))
    
    if not json_files:
        logging.warning("⚠️ Tidak ada file JSON di data/raw/ untuk diproses.")
        return
        
    logging.info(f"Menemukan {len(json_files)} file JSON. Memulai ekstraksi...")
    
    extracted_data = []
    
    for file in json_files:
        try:
            with open(file, 'r') as f:
                content = json.load(f)
                if content['status'] == 'success':
                    poll = content['data']['current']['pollution']
                    weat = content['data']['current']['weather']
                    
                    # Ekstrak data sesuai skema LK-03
                    extracted_data.append({
                        'timestamp': poll['ts'],
                        'aqi_us': poll['aqius'],
                        'main_pollutant': poll['mainus'],
                        'temperature_c': weat['tp'],
                        'humidity_pct': weat['hu']
                    })
        except Exception as e:
            logging.error(f"❌ Gagal membaca file {file}: {e}")
            
    if extracted_data:
        # Ubah ke Pandas DataFrame
        df = pd.DataFrame(extracted_data)
        
        # Konversi kolom timestamp ke tipe Datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Urutkan berdasarkan waktu dan hapus duplikasi (jika skrip dijalankan berkali-kali di jam yang sama)
        df = df.sort_values('timestamp').drop_duplicates(subset=['timestamp']).reset_index(drop=True)
        
        # Penanganan Missing Values menggunakan Forward Fill (jika ada)
        df = df.ffill()
        
        # Simpan hasil preprocessing ke data/interim/
        output_path = os.path.join(interim_dir, "jakarta_aqi_cleaned.csv")
        df.to_csv(output_path, index=False)
        
        logging.info(f"✅ Prapemrosesan selesai! Data tersimpan di: {output_path}")
        print(df.head()) # Tampilkan preview data
    else:
        logging.warning("⚠️ Tidak ada data valid yang berhasil diekstrak.")

if __name__ == "__main__":
    preprocess_data()