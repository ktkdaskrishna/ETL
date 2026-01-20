import os
from typing import Any, Dict, List

import requests
from requests.auth import HTTPBasicAuth


class AirflowClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("AIRFLOW_BASE_URL", "http://localhost:8080")
        self.username = os.getenv("AIRFLOW_USERNAME", "admin")
        self.password = os.getenv("AIRFLOW_PASSWORD", "admin")

    def _auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.username, self.password)

    def list_dags(self) -> List[Dict[str, Any]]:
        response = requests.get(
            f"{self.base_url}/api/v1/dags", auth=self._auth(), timeout=10
        )
        response.raise_for_status()
        return response.json().get("dags", [])

    def trigger_dag(self, dag_id: str, conf: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/v1/dags/{dag_id}/dagRuns",
            json={"conf": conf},
            auth=self._auth(),
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def list_dag_runs(self, dag_id: str) -> List[Dict[str, Any]]:
        response = requests.get(
            f"{self.base_url}/api/v1/dags/{dag_id}/dagRuns",
            auth=self._auth(),
            timeout=10,
        )
        response.raise_for_status()
        return response.json().get("dag_runs", [])
