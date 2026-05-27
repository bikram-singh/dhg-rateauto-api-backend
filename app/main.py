from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Import models ONCE here - before anything else
import app.models.department  # noqa: F401
import app.models.hospital    # noqa: F401
import app.models.vaccine     # noqa: F401
import app.models.pricing     # noqa: F401

from app.database import init_db, close_db
from app.routers import vaccines, hospitals, departments, pricing, ai_advisor


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="DHG Vaccine Fee API",
    description="Dummy Health Group — Vaccine Pricing & Management API",
    version="1.0.0",
    docs_url="/vaccinefee/api/docs",
    redoc_url="/vaccinefee/api/redoc",
    openapi_url="/vaccinefee/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vaccines.router,    prefix="/vaccinefee/api")
app.include_router(hospitals.router,   prefix="/vaccinefee/api")
app.include_router(departments.router, prefix="/vaccinefee/api")
app.include_router(pricing.router,     prefix="/vaccinefee/api")
app.include_router(ai_advisor.router,  prefix="/vaccinefee/api")


@app.get("/vaccinefee/api/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "dhg-vaccinefee-api"}


@app.get("/healthz", tags=["Health"])
async def liveness():
    return {"status": "ok"}


@app.get("/", tags=["Health"])
async def root():
    return JSONResponse(content={"status": "ok"}, status_code=200)