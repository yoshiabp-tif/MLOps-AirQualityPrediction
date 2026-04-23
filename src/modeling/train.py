import pandas as pd
import xgboost as xgb
import mlflow
import mlflow.xgboost
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import os

def prepare_data(filepath="data/interim/jakarta_aqi_cleaned.csv"):
    """Membaca data dan menyiapkan fitur & target untuk time-series"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} tidak ditemukan. Pastikan path benar.")
        
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    # Membuat target: Memprediksi AQI 1 Jam ke depan (Shift -1)
    df['target_aqi_next_hour'] = df['aqi_us'].shift(-1)
    
    # Hapus baris terakhir yang targetnya kosong (NaN) karena di-shift
    df = df.dropna() 

    # Memilih Fitur (X) dan Target (y)
    features = ['aqi_us', 'temperature_c', 'humidity_pct']
    X = df[features]
    y = df['target_aqi_next_hour']

    # Splitting data (Time-series tidak boleh diacak/shuffle)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    return X_train, X_test, y_train, y_test

def train_and_log(X_train, X_test, y_train, y_test, params, run_name):
    """Melatih model XGBoost dan mencatat metrik ke MLflow"""
    with mlflow.start_run(run_name=run_name):
        # 1. Logging Parameter (Sesuai Syarat LK-6)
        mlflow.log_params(params)

        # Melatih Model
        model = xgb.XGBRegressor(**params, random_state=42)
        model.fit(X_train, y_train)

        # Melakukan Prediksi
        predictions = model.predict(X_test)

        # Menghitung Error (Metrik)
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))

        # 2. Logging Metrik (Sesuai Syarat LK-6)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("RMSE", rmse)

        # 3. Logging Model Artefak (Sesuai Syarat LK-6)
        mlflow.xgboost.log_model(model, "xgboost-model")

        print(f"✅ {run_name} Selesai | MAE: {mae:.2f} | RMSE: {rmse:.2f}")

if __name__ == "__main__":
    print("Memuat dataset dan menyiapkan eksperimen...")
    X_train, X_test, y_train, y_test = prepare_data()

    # Inisialisasi Nama Eksperimen MLflow
    mlflow.set_experiment("Prediksi_AQI_Jakarta")

    # Eksekusi Variasi 1: Model Dasar
    params_1 = {"n_estimators": 50, "learning_rate": 0.1, "max_depth": 3}
    train_and_log(X_train, X_test, y_train, y_test, params_1, "Run_1_Basic")

    # Eksekusi Variasi 2: Pohon lebih dalam (Kompleks)
    params_2 = {"n_estimators": 100, "learning_rate": 0.1, "max_depth": 5}
    train_and_log(X_train, X_test, y_train, y_test, params_2, "Run_2_Deeper_Tree")

    # Eksekusi Variasi 3: Learning rate kecil, estimator banyak
    params_3 = {"n_estimators": 200, "learning_rate": 0.05, "max_depth": 4}
    train_and_log(X_train, X_test, y_train, y_test, params_3, "Run_3_Slow_Learning")

    print("Seluruh eksperimen MLflow berhasil dicatat.")