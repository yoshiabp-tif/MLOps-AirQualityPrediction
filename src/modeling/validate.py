import mlflow
from mlflow.tracking import MlflowClient

def validate_and_promote():
    client = MlflowClient()
    model_name = "AQI_Jakarta_Model"
    
    # 1. Ambil metrik performa dari model hasil training terbaru (Challenger)
    # Kita ambil daftarnya dulu untuk menghindari IndexError jika Staging kosong
    staging_versions = client.get_latest_versions(model_name, stages=["Staging"])
    
    if not staging_versions:
        # Failsafe: Jika train.py belum memindahkan ke 'Staging', coba cek di stage 'None' (default register)
        staging_versions = client.get_latest_versions(model_name, stages=["None"])
        
    if not staging_versions:
        print("❌ Error: Tidak ada model baru (Challenger) yang ditemukan di MLflow!")
        return
        
    latest_model = staging_versions[0]
    challenger_run = client.get_run(latest_model.run_id)
    # Menggunakan .get() agar aman dari KeyError jika metrik 'mae' belum tercatat
    challenger_metric = challenger_run.data.metrics.get("mae")
    
    if challenger_metric is None:
        print(f"❌ Error: Metrik 'mae' tidak ditemukan pada run Challenger ({latest_model.run_id})!")
        return

    # 2. Ambil metrik performa dari model lama yang sedang aktif (Champion)
    production_versions = client.get_latest_versions(model_name, stages=["Production"])
    
    # =========================================================================
    # KONDISI FAILSAFE: Jika BELUM ADA model di stage Production (Inisialisasi)
    # =========================================================================
    if not production_versions:
        print("ℹ️ Belum ada model lama di stage Production (Server MLflow masih kosong).")
        print(f"🚀 Model baru (Version {latest_model.version}) otomatis dipromosikan sebagai Champion pertama!")
        
        client.transition_model_version_stage(
            name=model_name, version=latest_model.version, stage="Production"
        )
        return

    # 3. Jika ada model Production lama, lakukan perbandingan metrik secara adil
    production_model = production_versions[0]
    champion_run = client.get_run(production_model.run_id)
    champion_metric = champion_run.data.metrics.get("mae")
    
    if champion_metric is None:
        print("⚠️ Warning: Metrik 'mae' Champion tidak ditemukan. Otomatis ganti dengan model baru.")
        champion_metric = float('inf') # Set nilai error tak terhingga agar challenger pasti menang

    print(f"📊 Champion MAE: {champion_metric} | Challenger MAE: {challenger_metric}")
    
    # 4. Keputusan Promosi Otomatis (Semakin kecil nilai MAE, semakin baik performanya)
    if challenger_metric < champion_metric:
        print("🔥 Challenger terbukti lebih akurat! Mempromosikan ke Production...")
        
        # Arsipkan model lama (Champion lama -> Archived)
        client.transition_model_version_stage(
            name=model_name, version=production_model.version, stage="Archived"
        )
        # Naikkan kelas model baru (Challenger -> Production)
        client.transition_model_version_stage(
            name=model_name, version=latest_model.version, stage="Production"
        )
    else:
        print("🔒 Performa Challenger tidak lebih baik. Champion bertahan di Production.")

if __name__ == "__main__":
    validate_and_promote()