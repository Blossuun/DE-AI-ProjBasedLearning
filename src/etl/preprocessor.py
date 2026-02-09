import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def preprocess_data(df):
    """
    AI 학습용 데이터로 만들기 위한 전처리(ETL의 Transform) 과정
    """
    df_clean = df.copy()
    
    # 1. 결측치(Null) 제거: 행동(action)이 없는 로그는 무의미하므로 삭제
    initial_count = len(df_clean)
    df_clean = df_clean.dropna(subset=['action'])
    print(f"Dropped {initial_count - len(df_clean)} rows with missing actions.")
    
    # 2. 이상치(Outlier) 처리: 가격이 0보다 작으면 데이터 오류로 간주하고 삭제
    # (실무에서는 평균값 대치 등을 쓰기도 하지만, 여기선 삭제로 진행)
    df_clean = df_clean[df_clean['price'] >= 0]
    
    # 3. 시간 순서 정렬 (시계열 데이터의 경우 중요)
    df_clean = df_clean.sort_values(by='timestamp').reset_index(drop=True)
    
    '''
    과제 1. 비즈니스 로직(이상치 필터링) 추가하기
    현재 코드는 음수 가격(price < 0)만 제거하고 있습니다. 하지만 현실에서는 실수로 입력된 너무 비싼 가격도 AI 모델의 학습을 방해(Gradient Explosion 등 유발)할 수 있습니다.

    미션: preprocess_data 함수를 수정하여 가격(price)이 450을 초과하는 데이터도 '이상치'로 간주하여 삭제하세요.

    목표: 단순한 오류(NULL) 처리뿐만 아니라, 도메인 지식에 기반한 데이터 클렌징을 경험합니다.
    '''

    df_clean = df_clean[df_clean["price"] < 450]
    
    '''
    과제 2. AI를 위한 파생 변수(Feature) 생성하기
    AI 모델은 2024-05-20 14:30:00 같은 타임스탬프 원본을 그대로 이해하지 못합니다. 보통 "오전/오후"나 "요일" 정보로 쪼개서 학습시킵니다.

    미션: df_clean 데이터프레임에 is_weekend 라는 새로운 컬럼(Feature)을 만드세요.

    timestamp가 토요일(5) 또는 일요일(6)이면 1, 평일이면 0을 넣습니다.

    힌트: df['timestamp'].dt.weekday를 활용하세요.

    목표: Data Engineering의 단계인 'Transform' 과정에서 AI 학습에 필요한 Feature를 미리 만들어주는 감각을 익힙니다.
    '''
    
    df_clean['is_weekend'] = df_clean['timestamp'].dt.weekday.map(lambda x: 1 if x >= 5 else 0)
    
    
    return df_clean