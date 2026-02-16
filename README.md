# Data to AI Engineering Pipeline Practice

로컬 환경에서 더러운(Dirty) 원본 데이터를 생성하고, 이를 정제하여 데이터베이스에 적재한 뒤, AI 모델 학습에 필요한 피처(Feature)를 추출하고 자동화하는 End-to-End 파이프라인 구축 프로젝트입니다.

## 🛠 Tech Stack
- **Language:** Python 3.13
- **Data Processing:** Pandas
- **Database:** SQLite
- **Automation:** Python `schedule`

## 🚀 진행된 과제 (Task History)

### Task 1: 데이터 생성 및 전처리 (ETL - Extract & Transform)
- `src/etl/generator.py`: 유저 행동 로그(click, purchase 등)를 시뮬레이션하여 생성. 가격 데이터에 의도적으로 노이즈(음수, 이상치)와 결측치 삽입.
- `src/etl/preprocessor.py`: AI 모델 학습의 안정성을 위해 `action`이 Null인 데이터 제거, `price`가 0 미만인 비정상 데이터 필터링 수행.

### Task 2: 데이터 적재 및 통계 추출 (ETL - Load & SQL Analysis)
- `src/database/connector.py`: 정제된 데이터를 SQLite RDB에 적재. 파이프라인 반복 실행 시 데이터가 누적되도록 `CREATE TABLE IF NOT EXISTS` 및 `append` 모드 적용.
- `src/analysis/analyzer.py`: SQL을 활용하여 AI 모델의 Feature로 사용될 수 있는 통계(유저별 총 구매액, 총 행동 횟수, 주말 구매 건수) 추출 로직 구현.

### Task 3: 파이프라인 자동화 (Automation)
- `run_scheduler.py`: 파이썬 내장 스케줄러를 도입하여 일정 주기(10초)마다 데이터 생성-정제-적재-분석 파이프라인이 자동으로 실행되는 데몬(Daemon) 프로세스 구축.