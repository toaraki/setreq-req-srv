# S2Iの考え方を意識し、依存関係をインストール
FROM registry.redhat.io/ubi9/python-39

WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
