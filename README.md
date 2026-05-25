# DHG Vaccine Fee API — Backend

FastAPI backend for the Dummy Health Group (DHG) vaccine pricing system.

## Stack
- **FastAPI** — REST API framework
- **SQLAlchemy (async)** — ORM with asyncpg
- **PostgreSQL 17** — via PSC (`10.10.0.3:5432`)
- **GCP Secret Manager** — DB password storage
- **GKE Autopilot** — Kubernetes deployment

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/vaccinefee/api/health` | Health check |
| GET | `/vaccinefee/api/vaccines` | List vaccines |
| POST | `/vaccinefee/api/vaccines` | Create vaccine |
| GET | `/vaccinefee/api/vaccines/{id}` | Get vaccine |
| PUT | `/vaccinefee/api/vaccines/{id}` | Update vaccine |
| DELETE | `/vaccinefee/api/vaccines/{id}` | Delete vaccine |
| GET | `/vaccinefee/api/hospitals` | List hospitals |
| POST | `/vaccinefee/api/hospitals` | Create hospital |
| GET | `/vaccinefee/api/departments` | List departments |
| POST | `/vaccinefee/api/departments` | Create department |
| GET | `/vaccinefee/api/pricing` | List pricing |
| POST | `/vaccinefee/api/pricing` | Create pricing |
| PUT | `/vaccinefee/api/pricing/{id}` | Update pricing |
| GET | `/vaccinefee/api/docs` | Swagger UI |

## Project Structure

```
dhg-vaccinefee-api/
├── app/
│   ├── main.py          # FastAPI app + CORS + routers
│   ├── config.py        # Settings + GCP Secret Manager
│   ├── database.py      # Async SQLAlchemy engine
│   ├── models/          # SQLAlchemy ORM models
│   ├── routers/         # API route handlers
│   └── schemas/         # Pydantic request/response schemas
├── Docker/
│   └── Dockerfile       # Multi-stage Python build
├── k8s/                 # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   └── serviceaccount.yaml
└── requirements.txt

.github/workflows/
├── ci.yml               # Lint → Test → Build → Push → Deploy
└── gke-deploy.yml       # Reusable GKE deploy workflow
```

## Prerequisites (GCP)

- `dhg-vaccinefee-sa` service account needs `roles/secretmanager.secretAccessor`
- PostgreSQL PSC endpoint reachable at `10.10.0.3:5432`
- Secret `dhg-vaccinefee-secret` in GCP Secret Manager with DB password
- Workload Identity binding for `dhg-vaccinefee-sa`

## Local Development

```bash
cd dhg-vaccinefee-api
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

Visit `http://localhost:8080/vaccinefee/api/docs` for Swagger UI.
