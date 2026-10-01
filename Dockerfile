FROM python:3.12.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV DEBUG=False
ENV PORT=8000
ENV LOG_FILE=data/logs/logs.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]