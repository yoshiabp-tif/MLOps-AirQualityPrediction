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
    """Membaca data dan menyiapkan fitur & target untuk time-series"""
    # [Fallback CI/CD] Jika dijalankan di GitHub Actions yang tidak memiliki data DVC lokal
    if not os.path.exists(filepath):
        print("⚠️ Data tidak ditemukan. Membuat data dummy khusus untuk simulasi CI/CD Pipeline...")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        dummy_df = pd.DataFrame({
            'timestamp': pd.date_range(start='2026-04-01', periods=100, freq='h'),
            'aqi_us': np.random.randint(50, 150, 100),
            'temperature_c': np.random.uniform(25, 35, 100),
            'humidity_pct': np.random.uniform(50, 90, 100)
        })
        dummy_df.to_csv(filepath, index=False)
        
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    df['target_aqi_next_hour'] = df['aqi_us'].shift(-1)
    df = df.dropna() 

    features = ['aqi_us', 'temperature_c', 'humidity_pct']
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
    THRESHOLD_MAE = 5.0  # Ambang batas performa dari LK-01
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