from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.api.router import api_router

app = FastAPI(
    title="TruckerEase Solution API",
    version="0.1.0",
    description="Backend API for TruckerEase Solution",
    lifespan=lifespan
)

app.include_router(api_router)