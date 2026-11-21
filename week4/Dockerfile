FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    OUTPUT_FILE=/data/repos.json

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY fetch_repos.py .

CMD ["python", "fetch_repos.py"]