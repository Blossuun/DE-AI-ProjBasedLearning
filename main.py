import os
from datetime import datetime
from src.etl.generator import generate_raw_data
from src.etl.preprocessor import preprocess_data
from src.database.connector import save_to_db
from src.analysis.analyzer import analyze_user_behavior
from src.storage.s3_uploader import upload_to_s3

def main():
    db_path = os.path.join("data", "database", "pipeline.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print("[Step 1] Raw Data 생성 중...")
    raw_df = generate_raw_data(num_rows=1000)
    
    print("[Step 2] 데이터 전처리 중...")
    clean_df = preprocess_data(raw_df)
    
    # [추가] Step 2.5: S3 데이터 레이크 적재
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    parquet_filename = f"user_logs_{current_time}.parquet"
    print(f"[Step 2.5] AWS S3 Data Lake 적재 중... ({parquet_filename})")
    upload_to_s3(clean_df, parquet_filename)
    
    print("[Step 3] DB 적재 중...")
    save_to_db(clean_df, db_path)
    
    analyze_user_behavior(db_path)
    print("\n🚀 파이프라인 배치 실행 완료!")

if __name__ == "__main__":
    main()