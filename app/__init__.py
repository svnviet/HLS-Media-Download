from fastapi import FastAPI
from .routers import router

app = FastAPI(
    # openapi_url="/openapi.json",  # URL for the OpenAPI schema
    docs_url="/swagger",  # URL for the Swagger UI
    # redoc_url="/redoc",  # URL for the ReDoc UI
)

app.include_router(router)
