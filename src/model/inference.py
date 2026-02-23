import os
import joblib
import pandas as pd

# 모델을 메모리에 한 번만 로드하기 위한 전역 변수 (캐싱 역할)
_model = None

def load_model():
    global _model
    model_path = "models/vip_predictor.pkl"
    if _model is None:
        if os.path.exists(model_path):
            _model = joblib.load(model_path)
            print("[Inference] AI 모델 로드 완료.")
        else:
            print("[Warning] 학습된 모델 파일이 없습니다. 예측을 건너뜁니다.")
    return _model

def extract_serving_features(df):
    """
    학습 때와 동일한 로직으로 서빙용 피처를 추출합니다. 
    (실무에서는 Feature Store를 통해 이 로직을 동기화합니다)
    """
    user_features = df.groupby('user_id').agg(
        click_count=('action', lambda x: (x == 'click').sum()),
        view_count=('action', lambda x: (x == 'view').sum()),
        cart_count=('action', lambda x: (x == 'add_to_cart').sum()),
        weekend_activity_count=('is_weekend', 'sum')
    ).reset_index()
    return user_features

def predict_vip(df):
    """
    현재 마이크로 배치 데이터의 유저들을 대상으로 VIP 여부를 예측합니다.
    """
    model = load_model()
    if model is None or df.empty:
        return
    
    # 피처 추출
    serving_features = extract_serving_features(df)
    
    # 모델 입력 변수 (X)
    X_serving = serving_features[['click_count', 'view_count', 'cart_count', 'weekend_activity_count']]
    
    # 추론 실행
    predictions = model.predict(X_serving)
    serving_features['predicted_is_vip'] = predictions
    
    # VIP로 예측된 유저 필터링
    vip_candidates = serving_features[serving_features['predicted_is_vip'] == 1]['user_id'].tolist()
    
    if vip_candidates:
        print(f"🎯 [AI Prediction] 실시간 VIP 예측 유저: {vip_candidates}")
    else:
        print("🎯 [AI Prediction] 이번 배치에는 VIP 예측 유저가 없습니다.")