FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app

ENV AIRFLOW_BASE_URL=http://airflow:8080 \
    AIRFLOW_USERNAME=admin \
    AIRFLOW_PASSWORD=admin

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
