import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


def generate_raw_data(num_rows=1000):
    """
    지저분한(Dirty) 가상의 유저 행동 로그를 생성합니다.
    """
    data = []
    actions = ['click', 'view', 'purchase', 'add_to_cart', None] # None은 결측치 시뮬레이션
    
    start_time = datetime.now()
    
    for i in range(num_rows):
        user_id = random.randint(1000, 1100)
        action = random.choices(actions, weights=[40, 30, 10, 15, 5])[0] # 5% 확률로 결측치 발생
        
        # 가격 데이터 (이상치 포함: 음수 가격 혹은 터무니없이 비싼 가격)
        if action == 'purchase':
            price = round(random.uniform(10, 500), 2)
        else:
            price = 0
            
        # 1% 확률로 데이터 오염 (가격이 -100이거나 문자열이 섞임)
        if random.random() < 0.01:
            price = -100 
            
        timestamp = start_time - timedelta(minutes=random.randint(0, 10000))
        
        data.append([user_id, action, price, timestamp])
        
    df = pd.DataFrame(data, columns=['user_id', 'action', 'price', 'timestamp'])
    return df