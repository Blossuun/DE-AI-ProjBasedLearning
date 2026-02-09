import os
from src.etl.generator import generate_raw_data
from src.etl.preprocessor import preprocess_data
from src.database.connector import save_to_db # 이 함수는 직접 만드셔야 합니다(아래 참고)

def main():
    # 1. 데이터 저장 경로 설정
    db_path = os.path.join("data", "database", "pipeline.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print("[Step 1] Raw Data 생성 중...")
    raw_df = generate_raw_data(num_rows=1000)
    
    print("[Step 2] 데이터 전처리 중...")
    clean_df = preprocess_data(raw_df)
    
    print("[Step 3] DB 적재 중...")
    # connector.py에 save_to_db(df, path) 함수가 있다고 가정
    save_to_db(clean_df, db_path)
    
    print("🚀 파이프라인 실행 완료!")

if __name__ == "__main__":
    main()