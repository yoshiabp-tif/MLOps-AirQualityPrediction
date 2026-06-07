import mlflow
from mlflow.tracking import MlflowClient
# ... (Import pustaka evaluasi metrik seperti sklearn)

def validate_and_promote():
    client = MlflowClient()
    model_name = "AQI_Jakarta_Model"
    
    # 1. Ambil metrik performa dari model lama yang sedang aktif (Champion)
    production_model = client.get_latest_versions(model_name, stages=["Production"])[0]
    champion_run = client.get_run(production_model.run_id)
    champion_metric = champion_run.data.metrics["mae"] # Menggunakan MAE sebagai indikator error AQI
    
    # 2. Ambil metrik performa dari model hasil training terbaru (Challenger)
    # (Skrip train.py secara otomatis mendaftarkan model baru ke status 'Staging')
    latest_model = client.get_latest_versions(model_name, stages=["Staging"])[0]
    challenger_run = client.get_run(latest_model.run_id)
    challenger_metric = challenger_run.data.metrics["mae"]
    
    print(f"Champion MAE: {champion_metric} | Challenger MAE: {challenger_metric}")
    
    # 3. Keputusan Promosi Otomatis (Semakin kecil nilai MAE, semakin baik performanya)
    if challenger_metric < champion_metric:
        print("Challenger terbukti lebih akurat! Mempromosikan ke Production...")
        # Arsipkan model lama (Champion lama -> Archived)
        client.transition_model_version_stage(
            name=model_name, version=production_model.version, stage="Archived"
        )
        # Naikkan kelas model baru (Challenger -> Production)
        client.transition_model_version_stage(
            name=model_name, version=latest_model.version, stage="Production"
        )
    else:
        print("Performa Challenger tidak lebih baik. Champion bertahan di Production.")

if __name__ == "__main__":
    validate_and_promote()