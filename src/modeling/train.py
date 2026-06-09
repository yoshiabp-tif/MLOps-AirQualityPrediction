import pandas as pd
import xgboost as xgb
import mlflow
import mlflow.xgboost
from mlflow.client import MlflowClient
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import os

def prepare_data(filepath="data/interim/jakarta_aqi_cleaned.csv"):
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    # 🚀 REKAYASA FITUR BARU (FEATURE ENGINEERING)
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # Fitur Lag (Riwayat masa lalu)
    df['aqi_lag_2'] = df['aqi_us'].shift(1) # Nilai jam sebelumnya
    df['aqi_diff'] = df['aqi_us'].diff()     # Tren kenaikan/penurunan
    
    # Target prediksi jam berikutnya
    df['target_aqi_next_hour'] = df['aqi_us'].shift(-1)
    
    # Hapus baris kosong akibat proses shifting dan diff
    df = df.dropna() 

    # Daftarkan semua pasukan fitur baru ke dalam model
    features = ['aqi_us', 'temperature_c', 'humidity_pct', 'hour', 'day_of_week', 'aqi_lag_2', 'aqi_diff']
    X = df[features]
    y = df['target_aqi_next_hour']
    
    return train_test_split(X, y, test_size=0.2, shuffle=False)

def train_and_evaluate(X_train, X_test, y_train, y_test, params, run_name):
    """Melatih model XGBoost dan mencatat metrik ke MLflow"""
    with mlflow.start_run(run_name=run_name) as run:
        mlflow.log_params(params)
        model = xgb.XGBRegressor(**params, random_state=42)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))

        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("RMSE", rmse)
        mlflow.xgboost.log_model(model, "xgboost-model")
        
        return run.info.run_id, mae

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = prepare_data()
    mlflow.set_experiment("Prediksi_AQI_Jakarta")

    print("Memulai pelatihan otomatis (CI/CD)...")
    # Perubahan parameter kecil sebagai bentuk "Simulasi Perubahan" (Tahap 6)
    params = {"n_estimators": 75, "learning_rate": 0.05, "max_depth": 4}
    
    run_id, mae = train_and_evaluate(X_train, X_test, y_train, y_test, params, "Run_Automated_Pipeline")

    # TAHAP 3: Model Evaluation & Validation
    THRESHOLD_MAE = 50.0
    print(f"\n📊 Hasil Evaluasi -> MAE: {mae:.2f} (Ambang Batas Maksimal: {THRESHOLD_MAE})")

    # TAHAP 4: Auto-Registry Update
    if mae <= THRESHOLD_MAE:
        print("✅ Evaluasi SUKSES! Model lolos validasi. Mendaftarkan ke Model Registry...")
        model_uri = f"runs:/{run_id}/xgboost-model"
        model_name = "AQI_Jakarta_Model"

        # Mendaftarkan Model
        registered_model = mlflow.register_model(model_uri, model_name)

        # Transisi ke Staging secara otomatis menggunakan MLflow Client
        client = MlflowClient()
        client.transition_model_version_stage(
            name=model_name,
            version=registered_model.version,
            stage="Staging"
        )
        print(f"Model versi {registered_model.version} berhasil ditransisikan ke status 'Staging' secara otomatis!")
    else:
        print("❌ Evaluasi GAGAL! Performa model lebih buruk dari ambang batas. Registrasi dibatalkan.")