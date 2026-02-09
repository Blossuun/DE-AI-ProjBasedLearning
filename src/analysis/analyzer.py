import sqlite3
import pandas as pd

def analyze_user_behavior(db_path):
    """
    DB에 저장된 로그 데이터를 분석하여 리포트를 출력합니다.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n--- [Analysis Report] ---")

    # ---------------------------------------------------------
    # 과제 1: 유저별 구매 총액(Total Spend) 및 행동 횟수 상위 5명
    # AI 모델의 Feature: "이 사람이 얼마나 가치 있는 고객인가?"
    # ---------------------------------------------------------
    query_top_users = """
    SELECT 
        user_id, 
        SUM(price) as total_spend, 
        COUNT(action) as action_count
    FROM user_logs
    GROUP BY user_id
    ORDER BY total_spend DESC
    LIMIT 5
    """
    
    print("1. Top 5 VIP Users (High Spenders):")
    cursor.execute(query_top_users)
    top_users = cursor.fetchall()
    
    for rank, (uid, spend, count) in enumerate(top_users, 1):
        print(f"   Rank {rank}: User {uid} | Total Spend: ${spend:.2f} | Actions: {count}")

    # ---------------------------------------------------------
    # 과제 2: 주말(is_weekend=1)에 발생한 'purchase' 건수
    # AI 모델의 Feature: "주말 프로모션에 반응하는가?"
    # ---------------------------------------------------------
    query_weekend_purchase = """
    SELECT COUNT(*) 
    FROM user_logs 
    WHERE is_weekend = 1 AND action = 'purchase'
    """
    
    cursor.execute(query_weekend_purchase)
    weekend_count = cursor.fetchone()[0]
    print(f"\n2. Total Purchases on Weekends: {weekend_count} orders")

    conn.close()