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

## Local Troubleshooting (Mac + Docker Desktop)
If `docker compose up --build` fails on macOS, verify the following before retrying:

1. **Docker Desktop is running**: the whale icon should show "Docker Desktop is running".
2. **Dockerfile does not run pip as root**: `airflow-ui/Dockerfile` should not include `USER root` or `RUN pip install ...`.
3. **Compose file has no `version` key**: modern Docker Compose ignores `version`, but removing it avoids warnings.

If your local files still show the old content, update your branch to the latest remote:
```bash
git fetch origin
git reset --hard origin/main
```

If you are working on a feature branch instead of `main`, list remote branches first and
reset to the exact branch name you intend to use:
```bash
git branch -r
git reset --hard origin/<exact-remote-branch-name>
```
