FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app
COPY data/ethereum_txs.csv /app/data/ethereum_txs.csv

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]