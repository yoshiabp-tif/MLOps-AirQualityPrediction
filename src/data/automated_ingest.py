import requests
import pandas as pd
import datetime
import os

# Konfigurasi API IQAir berdasarkan data akunmu
API_KEY = "b7494306-68a0-467f-992b-8831c664fc42"
URL = f"http://api.airvisual.com/v2/city?city=Jakarta&state=Jakarta&country=Indonesia&key={API_KEY}"
CSV_PATH = "data/interim/jakarta_aqi_cleaned.csv"

def fetch_and_append_data():
    try:
        # 1. Ambil data real-time dari IQAir
        response = requests.get(URL)
        res_json = response.json()
        
        if res_json["status"] == "success":
            data_node = res_json["data"]["current"]
            
            # 2. Ekstrak fitur yang sesuai dengan kebutuhan XGBoost kamu
            new_record = {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:00:00+00:00"),
                "aqi_us": data_node["pollution"]["aqius"],
                "main_pollutant": data_node["pollution"]["mainus"],
                "temperature_c": data_node["weather"]["tp"],
                "humidity_pct": data_node["weather"]["hu"]
            }
            
            # 3. Masukkan ke dataframe
            new_df = pd.DataFrame([new_record])
            
            # 4. Append (gabungkan) ke file CSV lama tanpa menghapus isinya
            if os.path.exists(CSV_PATH):
                old_df = pd.read_csv(CSV_PATH)
                if new_record["timestamp"] not in old_df["timestamp"].values:
                    combined_df = pd.concat([old_df, new_df], ignore_index=True)
                    combined_df.to_csv(CSV_PATH, index=False)
                    print(f"✅ Sukses menambah data jam: {new_record['timestamp']}")
            else:
                # 👇 SISIPKAN KODE SAKTI INI DI SINI 👇
                os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
                
                new_df.to_csv(CSV_PATH, index=False)
                print("✅ Sukses membuat berkas data baru di cloud.")
                
    except Exception as e:
        print(f"❌ Ingestion Gagal: {e}")

if __name__ == "__main__":
    fetch_and_append_data()