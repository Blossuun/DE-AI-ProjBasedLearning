# .python-version에 맞춘 베이스 이미지 사용
FROM python:3.13-slim

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

ENV PYTHONUNBUFFERED=1

# 가장 빠른 패키지 설치 도구인 uv 설치
RUN pip install uv

# 패키지 관리를 위한 파일만 먼저 복사 (캐시 활용 최적화)
COPY pyproject.toml uv.lock ./

# uv를 사용하여 의존성 설치 (컨테이너 환경이므로 가상환경 없이 시스템에 직접 설치)
RUN uv pip install --system -r pyproject.toml

# 소스 코드 전체 복사
COPY . .

# 스케줄러 실행
CMD ["python", "run_scheduler.py"]