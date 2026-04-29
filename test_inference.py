import mlflow.pyfunc
import pandas as pd

print("Mencari model berstatus Production di Model Registry...")

# Memanggil model langsung berdasarkan Stage-nya (Production)
model_uri = "models:/AQI_Jakarta_Model/Production"

try:
    model = mlflow.pyfunc.load_model(model_uri)
    print("✅ Model Production berhasil dimuat!")
    
    # Menyiapkan 1 baris data cuaca tiruan (suhu 31C, kelembapan 70%, AQI saat ini 85)
    print("\nMensimulasikan data sensor saat ini...")
    dummy_data = pd.DataFrame({
        'aqi_us': [85],
        'temperature_c': [31],
        'humidity_pct': [70]
    })
    
    # Melakukan prediksi inferensi
    prediction = model.predict(dummy_data)
    print(f"HASIL INFERENSI: Prediksi AQI 1 Jam ke depan adalah {prediction[0]:.2f}")
    
except Exception as e:
    print(f"❌ Gagal memuat model. Error: {e}")