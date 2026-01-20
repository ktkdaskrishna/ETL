# Unified UI Platform for Airflow and FastAPI

## Overview
The Unified UI Platform delivers a cohesive, guided experience for building data pipelines in Apache Airflow and publishing APIs in FastAPI. The solution ships as two Docker images: one for Airflow workflow orchestration and another for FastAPI-based API management. Users move from data ingestion to API deployment through a single, consistent UI flow.

## Goals
- Provide a guided workflow UI to define, run, and monitor Airflow DAGs.
- Provide a UI to create, publish, and manage FastAPI endpoints.
- Enable data flow from Airflow outputs to FastAPI endpoints via a shared integration layer.
- Package each module into its own Docker image for independent scaling.

## Non-Goals
- Implementing a full-featured Airflow UI replacement (we leverage Airflow Webserver UI).
- Providing production-grade auth/SSO (templates include placeholders).
- Building a full API gateway or data catalog.

## Personas
- **Data Engineer:** Creates and monitors ingestion/transformation workflows.
- **API Engineer:** Publishes and maintains API endpoints for consumers.
- **Ops Engineer:** Deploys and maintains containerized services.

## User Experience
1. User lands on the Unified UI entry point (FastAPI UI).
2. User creates or triggers a workflow in Airflow (Airflow Webserver UI or FastAPI UI trigger).
3. User monitors workflow status and logs.
4. User publishes endpoints that serve curated outputs from Airflow tasks.

## Functional Requirements
### Airflow UI Module
- Display Airflow UI for DAG creation, execution, and monitoring.
- Provide example DAG templates for ingestion and transformation.
- Expose REST API for programmatic DAG triggers (Airflow API v1).

### FastAPI UI Module
- Provide a UI for managing API endpoints and templates.
- Offer workflow-triggering and status-checking capabilities against Airflow.
- Provide example endpoints that serve output artifacts from Airflow.

### Integration Layer
- FastAPI UI communicates with Airflow REST API.
- Shared metadata contract for workflow outputs (e.g., dataset IDs, output locations).
- Environment variable configuration for service discovery.

## API & Data Contracts
- **Airflow Trigger**: POST `/api/v1/dags/{dag_id}/dagRuns`
- **Airflow Status**: GET `/api/v1/dags/{dag_id}/dagRuns`
- **Output Metadata**: JSON with fields `{dataset_id, storage_uri, schema_version}`

## Architecture
- **Airflow Docker Image**: Runs scheduler + webserver.
- **FastAPI Docker Image**: Runs UI + API management interface.
- **Integration**: HTTP REST calls from FastAPI to Airflow.

## Deployment
- Two Docker images built independently.
- Optional Docker Compose to run both with shared network.
- Env vars for Airflow URL, API auth token, and artifact storage.

## Security & Compliance
- Airflow API authentication enabled via standard configs.
- FastAPI UI supports token-based auth (placeholder in templates).

## Metrics & Observability
- Airflow provides DAG metrics and logs.
- FastAPI UI includes health endpoint and basic usage tracking (template).

## Risks
- Airflow API auth variations across versions.
- Cross-service networking in container environments.

## Milestones
1. Docker templates for Airflow and FastAPI.
2. Basic UI pages and integration endpoints.
3. Sample workflows and API endpoints.

## Open Questions
- Which artifact storage backend should be used (S3, GCS, local)?
- Should API endpoints be generated dynamically or via templates?
