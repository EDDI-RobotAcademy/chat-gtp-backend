# Python 3.12 이미지 기반
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential
    default-libmysqlclient-dev \
    pkg-config
    && rm -rf /var/lib/apt/lists/*

# 필요한 패키지 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# wait-for-it.sh 스크립트 복사
COPY wait-for-it.sh /app/wait-for-it.sh

RUN chmod +x /app/wait-for-it.sh

# 프로젝트 코드 복사
COPY . /app/

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1


# wait-for-it.sh 스크립트를 사용하여 MySQL 컨테이너가 준비될 때까지 대기
CMD ["/app/wait-for-it.sh", "db:3306", "--", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
