from typing import Any, Dict

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.airflow_client import AirflowClient

app = FastAPI(title="Unified UI Platform")
templates = Jinja2Templates(directory="app/templates")
client = AirflowClient()


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    dags = client.list_dags()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "dags": dags,
        },
    )


@app.post("/trigger")
def trigger_dag(
    dag_id: str = Form(...),
    dataset_id: str = Form("sample_dataset"),
    storage_uri: str = Form("s3://bucket/path"),
) -> RedirectResponse:
    conf: Dict[str, Any] = {"dataset_id": dataset_id, "storage_uri": storage_uri}
    client.trigger_dag(dag_id, conf)
    return RedirectResponse(url="/", status_code=303)


@app.get("/runs/{dag_id}", response_class=HTMLResponse)
def list_runs(request: Request, dag_id: str) -> HTMLResponse:
    dag_runs = client.list_dag_runs(dag_id)
    return templates.TemplateResponse(
        "runs.html",
        {
            "request": request,
            "dag_id": dag_id,
            "dag_runs": dag_runs,
        },
    )


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}
