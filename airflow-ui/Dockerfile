FROM apache/airflow:2.8.3

COPY dags/ /opt/airflow/dags/

ENV AIRFLOW__CORE__LOAD_EXAMPLES=False \
    AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True \
    AIRFLOW__API__AUTH_BACKENDS=airflow.api.auth.backend.basic_auth

EXPOSE 8080

CMD ["bash", "-c", "airflow db init && airflow users create --role Admin --username admin --password admin --firstname Admin --lastname User --email admin@example.com && airflow webserver"]
