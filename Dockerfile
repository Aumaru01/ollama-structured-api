FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ARG API_PORT=8000
ENV API_PORT=${API_PORT}

EXPOSE ${API_PORT}

CMD uvicorn app:app --host 0.0.0.0 --port ${API_PORT}
