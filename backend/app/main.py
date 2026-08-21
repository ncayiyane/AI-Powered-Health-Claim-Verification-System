from fastapi import FastAPI

from app.api.routes import router as claim_router


app = FastAPI(
    title="AI-Powered Health Claim Verification System",
    description=(
        "An AI-powered system that verifies health-related claims "
        "using evidence retrieval and large language models."
    ),
    version="1.0.0",
)


app.include_router(claim_router)


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