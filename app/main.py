from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Import models ONCE here - before anything else
import app.models.department  # noqa: F401
import app.models.hospital    # noqa: F401
import app.models.vaccine     # noqa: F401
import app.models.pricing     # noqa: F401
import app.models.user        # noqa: F401

from app.database import init_db, close_db
from app.routers import vaccines, hospitals, departments, pricing, ai_advisor, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="DHG Vaccine Fee API",
    description="""
## 🏥 Dummy Health Group — Vaccine Pricing & Management API

### Overview
This API powers the DHG Vaccine Pricing Dashboard, providing real-time vaccine pricing data
across **108 hospitals** in India, USA, and internationally.

### Features
- 🔐 **JWT Authentication** — Secure role-based access (Admin/Viewer)
- 💉 **65 Vaccines** — Global coverage with real manufacturers
- 🏥 **108 Hospitals** — India, USA, London, Tokyo, Singapore and more
- 💰 **5,400+ Pricing Records** — Realistic market prices
- 🤖 **AI Advisor** — Claude-powered vaccine recommendations

### Authentication
Use the `/auth/login` endpoint to get a JWT token.
Include it in headers: `Authorization: Bearer <token>`

### Quick Start
1. `POST /vaccinefee/api/auth/login` — Get JWT token
2. `GET /vaccinefee/api/vaccines/` — List all vaccines
3. `GET /vaccinefee/api/pricing/` — Get pricing data
    """,
    version="2.0.0",
    contact={
        "name": "Bikram Singh — DHG Dev Team",
        "email": "support@dummyhealthgroup.com",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/vaccinefee/api/docs",
    redoc_url="/vaccinefee/api/redoc",
    openapi_url="/vaccinefee/api/openapi.json",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Authentication", "description": "JWT login, user management and access control"},
        {"name": "Vaccines",       "description": "Vaccine catalog with manufacturer information"},
        {"name": "Hospitals",      "description": "Hospital directory across India and internationally"},
        {"name": "Departments",    "description": "Medical department categories"},
        {"name": "Pricing",        "description": "Vaccine pricing data with stock and insurance info"},
        {"name": "AI Advisor",     "description": "Claude AI-powered vaccine recommendations"},
        {"name": "Health",         "description": "Health check endpoints for load balancer"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,        prefix="/vaccinefee/api")
app.include_router(vaccines.router,    prefix="/vaccinefee/api")
app.include_router(hospitals.router,   prefix="/vaccinefee/api")
app.include_router(departments.router, prefix="/vaccinefee/api")
app.include_router(pricing.router,     prefix="/vaccinefee/api")
app.include_router(ai_advisor.router,  prefix="/vaccinefee/api")


@app.get("/vaccinefee/api/health", tags=["Health"])
async def health_check():
    """Check API health status"""
    return {"status": "healthy", "service": "dhg-vaccinefee-api", "version": "2.0.0"}


@app.get("/healthz", tags=["Health"])
async def liveness():
    """Kubernetes liveness probe"""
    return {"status": "ok"}


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return JSONResponse(content={"status": "ok", "docs": "/vaccinefee/api/docs"}, status_code=200)
