FROM python:3.10

EXPOSE 8000
WORKDIR /app

COPY requirements* /app/backend/

RUN pip install --upgrade pip && pip install -r /app/backend/requirements.txt

CMD ["uvicorn", "app.api:app", "--host 0.0.0.0"]