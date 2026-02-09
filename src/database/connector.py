import pandas as pd
import numpy as np
import sqlite3

def save_to_db(clean_df, db_path):

    # 1. DB 연결 (파일로 저장됨: 'my_data_pipeline.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 2. 테이블 생성 (DDL)
    # 이미 테이블이 있다면 삭제하고 새로 만듭니다 (실습용 리셋)
    cursor.execute("DROP TABLE IF EXISTS user_logs")

    # AI 학습에 필요한 스키마 정의
    # user_id: 정수형, action: 문자열, price: 실수형, timestamp: 문자열, is_weekend: 정수형
    create_table_query = """
    CREATE TABLE user_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        price REAL,
        timestamp TEXT,
        is_weekend INTEGER
    )
    """
    cursor.execute(create_table_query)
    print("테이블 생성 완료: user_logs")

    # clean_df 데이터를 'user_logs' 테이블에 저장
    # if_exists='append': 테이블이 이미 있으면 데이터를 추가합니다.
    clean_df.to_sql('user_logs', conn, if_exists='append', index=False)

    print(f"{len(clean_df)} 개의 데이터가 DB에 적재되었습니다.")

    # 검증 1: 상위 5개 데이터 조회
    print("\n[DB 조회 결과 - 상위 5개]")
    cursor.execute("SELECT * FROM user_logs LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # 연결 종료
    conn.close()