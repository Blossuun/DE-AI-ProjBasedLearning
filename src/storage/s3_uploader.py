import os
import boto3
from dotenv import load_dotenv

# 로컬 테스트 .env 파일을 읽어옵니다. (도커 환경에서는 환경 변수가 직접 주입됨)
load_dotenv()

def upload_to_s3(df, file_name):
    """
    Pandas DataFrame을 Parquet 포맷으로 변환 후 AWS S3에 업로드합니다.
    """
    bucket_name = os.getenv('S3_BUCKET_NAME')
    if not bucket_name:
        print("[Warning] S3_BUCKET_NAME 환경 변수가 없습니다. 업로드를 건너뜁니다.")
        return

    # 컨테이너 내 임시 파일 저장 경로
    local_path = f"/tmp/{file_name}"
    
    # Parquet 저장 (컬럼 기반 저장소로, CSV 대비 용량과 읽기 속도가 AI 학습에 압도적으로 유리함)
    df.to_parquet(local_path, index=False)

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION')
        )
        
        # S3 내부의 폴더 구조(Prefix) 지정
        s3_key = f"processed_logs/{file_name}"
        s3_client.upload_file(local_path, bucket_name, s3_key)
        
        print(f"✅ S3 Upload Complete: s3://{bucket_name}/{s3_key}")
        
    except Exception as e:
        print(f"❌ S3 Upload Failed: {e}")
    finally:
        # 업로드 완료 후 임시 파일 삭제하여 컨테이너 용량 확보
        if os.path.exists(local_path):
            os.remove(local_path)