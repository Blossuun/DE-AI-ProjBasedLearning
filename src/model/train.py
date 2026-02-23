import os
import pandas as pd
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 환경 변수 로드 (AWS 자격 증명)
load_dotenv()

def load_data_from_s3(bucket_name, prefix="processed_logs/"):
    """
    S3 버킷에서 Parquet 파일들을 읽어와 하나의 DataFrame으로 병합합니다.
    """
    import boto3
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION')
    )
    
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' not in response:
        print("S3에 학습할 데이터가 없습니다.")
        return pd.DataFrame()

    df_list = []
    for obj in response['Contents']:
        key = obj['Key']
        if key.endswith(".parquet"):
            # s3fs 라이브러리를 통해 pandas에서 직접 S3 경로 읽기 지원
            s3_path = f"s3://{bucket_name}/{key}"
            df = pd.read_parquet(
                s3_path, 
                storage_options={
                    "key": os.getenv('AWS_ACCESS_KEY_ID'),
                    "secret": os.getenv('AWS_SECRET_ACCESS_KEY')
                }
            )
            df_list.append(df)
            
    print(f"총 {len(df_list)}개의 Parquet 파일을 병합했습니다.")
    return pd.concat(df_list, ignore_index=True)

def feature_engineering(df):
    """
    Raw 로그 데이터를 모델이 학습할 수 있는 유저 단위(User-level) 피처로 변환합니다.
    """
    # 1. 유저별 총 구매액 및 클릭/뷰/장바구니 횟수 집계
    user_features = df.groupby('user_id').agg(
        total_spend=('price', 'sum'),
        click_count=('action', lambda x: (x == 'click').sum()),
        view_count=('action', lambda x: (x == 'view').sum()),
        cart_count=('action', lambda x: (x == 'add_to_cart').sum()),
        weekend_activity_count=('is_weekend', 'sum')
    ).reset_index()

    # 2. 타겟(Target) 변수 생성: 총 구매액이 500 이상이면 VIP(1), 아니면 Normal(0)
    user_features['is_vip'] = (user_features['total_spend'] >= 500).astype(int)
    
    return user_features

def main():
    bucket_name = os.getenv('S3_BUCKET_NAME')
    print("[1/4] S3 데이터 레이크에서 원본 로그 로드 중...")
    raw_df = load_data_from_s3(bucket_name)
    
    if raw_df.empty:
        return

    print("[2/4] AI 모델용 Feature Engineering 수행 중...")
    features_df = feature_engineering(raw_df)
    
    # 학습 피처(X)와 타겟 변수(y) 분리 (total_spend는 정답과 직결되므로 제외)
    X = features_df[['click_count', 'view_count', 'cart_count', 'weekend_activity_count']]
    y = features_df['is_vip']

    # 학습/테스트 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("[3/4] Random Forest 모델 학습 중...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print("[4/4] 모델 평가 및 저장...")
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print("\n[Classification Report]")
    print(classification_report(y_test, y_pred, zero_division=0))

    # 학습된 모델을 로컬에 저장 (향후 추론/Serving 파이프라인에서 사용)
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/vip_predictor.pkl")
    print("✅ 모델 저장 완료: models/vip_predictor.pkl")

if __name__ == "__main__":
    main()