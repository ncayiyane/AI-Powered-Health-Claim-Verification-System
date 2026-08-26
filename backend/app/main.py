from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as claim_router


app = FastAPI(
    title="AI-Powered Health Claim Verification System",
    description=(
        "An AI-powered system that verifies health-related claims "
        "using evidence retrieval and large language models."
    ),
    version="1.0.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# API Routes
# --------------------------------------------------

app.include_router(claim_router)


# --------------------------------------------------
# Health / Root Endpoints
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI-Powered Health Claim Verification System API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }