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
4. **Run Compose from your Mac terminal, not inside a container**: if your prompt looks like `sh-3.2#`,
   run `exit` until you return to your Mac shell (e.g., `MacBook-Pro:ETL user$`), then run Docker Compose there.
5. **Docker Compose is installed**: run `docker compose version`. If you see
   `docker: 'compose' is not a docker command`, install or upgrade Docker Desktop, or use the legacy
   `docker-compose` binary if it exists (`docker-compose --version`).

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

### Optional Python Dependencies in the Airflow Image
The base image already includes Airflow. If you need extra Python packages, install
them as the `airflow` user to avoid the root pip error:

```dockerfile
FROM apache/airflow:2.8.3

COPY requirements.txt /requirements.txt

USER airflow
RUN pip install --no-cache-dir -r /requirements.txt
```

If you must install OS packages, switch to `root` first, then return to `airflow`
before running `pip install`.

### Manual Fix (if you cannot reset the branch)
If you cannot reset or are unsure which branch has the fix, you can manually update
the two files below to match the working configuration.

1. **Update `airflow-ui/Dockerfile`** (remove root pip install):
   ```bash
   cat > airflow-ui/Dockerfile <<'EOF'
   FROM apache/airflow:2.8.3

   COPY dags/ /opt/airflow/dags/

   ENV AIRFLOW__CORE__LOAD_EXAMPLES=False \
       AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True \
       AIRFLOW__API__AUTH_BACKENDS=airflow.api.auth.backend.basic_auth

   EXPOSE 8080

   CMD ["bash", "-c", "airflow db init && airflow users create --role Admin --username admin --password admin --firstname Admin --lastname User --email admin@example.com && airflow webserver"]
   EOF
   ```

2. **Update `docker-compose.yml`** (remove deprecated `version` key):
   ```bash
   cat > docker-compose.yml <<'EOF'
   services:
     airflow:
       build: ./airflow-ui
       ports:
         - "8080:8080"
       environment:
         - AIRFLOW__API__AUTH_BACKENDS=airflow.api.auth.backend.basic_auth
     fastapi-ui:
       build: ./fastapi-ui
       ports:
         - "8000:8000"
       environment:
         - AIRFLOW_BASE_URL=http://airflow:8080
         - AIRFLOW_USERNAME=admin
         - AIRFLOW_PASSWORD=admin
       depends_on:
         - airflow
   EOF
   ```

3. **Rebuild cleanly**:
   ```bash
   docker compose build --no-cache
   docker compose up
   ```
