FROM python:3.12-slim-bookworm
# dir
WORKDIR /app
# requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# sub ranks
COPY worker.py .
# 强制无缓冲实时输出。
ENV PYTHONUNBUFFERED=1