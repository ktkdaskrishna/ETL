# Integration Template

## Overview
The FastAPI UI uses Airflow's REST API to trigger workflows and list DAG runs. Communication is performed via HTTP Basic Auth over the Airflow Webserver API.

## Environment Variables
- `AIRFLOW_BASE_URL`: Base URL of Airflow Webserver (e.g., `http://airflow:8080`).
- `AIRFLOW_USERNAME`: Airflow UI username.
- `AIRFLOW_PASSWORD`: Airflow UI password.

## Data Flow
1. User submits a DAG trigger request in FastAPI UI.
2. FastAPI sends a POST request to Airflow `/api/v1/dags/{dag_id}/dagRuns`.
3. Airflow executes the workflow and writes output artifacts.
4. FastAPI UI surfaces run statuses and provides API endpoint templates for consuming outputs.

## Extension Points
- Replace Basic Auth with OAuth/SSO.
- Store output metadata in a shared database or object storage.
- Add an API builder UI for defining schema and versioning.
