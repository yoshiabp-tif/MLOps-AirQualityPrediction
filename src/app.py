from fastapi import FastAPI, Request
import mlflow.pyfunc
import pandas as pd
import time
from prometheus_client import make_asgi_app, Counter, Histogram

app = FastAPI(title="AQI Prediction API with Observability")

# 1. Definisi Sensor Metrik Prometheus
REQUEST_COUNT = Counter("api_requests_total", "Total jumlah request inferensi masuk")
LATENCY = Histogram("api_inference_latency_seconds", "Waktu latensi pemrosesan inferensi (detik)")
PREDICTION_DISTRIBUTION = Histogram("model_prediction_aqi", "Distribusi nilai tebakan AQI untuk deteksi Data Drift")

# 2. Muat Model Langsung dari MLflow Registry
model_uri = "models:/AQI_Jakarta_Model/Production"
try:
    # 1. Coba jalur normal via Registry Network
    model = mlflow.pyfunc.load_model(model_uri)
except Exception as e:
    print(f"⚠️ MLflow Registry network load failed: {e}")
    print("🚀 Activating Smart Local Disk Fallback...")
    import glob
    import os
    
    # Cari semua file konfigurasi MLmodel yang ada di penyimpanan disk lokal
    mlmodel_files = glob.glob("mlruns/**/MLmodel", recursive=True) + glob.glob("/app/mlruns/**/MLmodel", recursive=True)
    
    if mlmodel_files:
        # Ambil folder model yang paling baru gres dimodifikasi/dibuat hari ini
        latest_mlmodel = max(mlmodel_files, key=os.path.getmtime)
        model_dir = os.path.dirname(latest_mlmodel)
        print(f"📦 Found fresh model on local drive! Loading directly from: {model_dir}")
        model = mlflow.pyfunc.load_model(model_dir)
    else:
        raise RuntimeError("❌ Tragis! Tidak ada file MLmodel apa pun baik di Registry maupun di disk lokal.")

# 3. Ekspos Jalur /metrics untuk Disedot oleh Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# 4. Pintu Masuk Request Prediksi
@app.post("/invocations")
async def predict(request: Request):
    REQUEST_COUNT.inc() # Menghitung throughput
    start_time = time.time() # Mulai stopwatch
    
    # Ekstrak format JSON bawaan MLflow
    data = await request.json()
    columns = data['dataframe_split']['columns']
    rows = data['dataframe_split']['data']
    df = pd.DataFrame(rows, columns=columns)
    
    # Eksekusi Tebakan
    predictions = model.predict(df)
    pred_value = float(predictions[0])
    
    # Catat angka tebakan ke metrik untuk mendeteksi anomali/drift
    PREDICTION_DISTRIBUTION.observe(pred_value)
    
    # Hentikan stopwatch dan catat latensi
    latency = time.time() - start_time
    LATENCY.observe(latency)
    
    return {"predictions": predictions.tolist()}