from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.infrastructure.api.routers import files
from src.infrastructure.persistence.database import engine, Base
from src.domain.exceptions import BaseAppException, FileNotFoundError, AnalysisNotFoundError

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Document Versioning Service",
    description="Mini-service for storing documents with versioning, metadata, and basic AI analysis",
    version="1.0.0"
)

app.include_router(files.router)


# Exception handlers
@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(request: Request, exc: FileNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


@app.exception_handler(AnalysisNotFoundError)
async def analysis_not_found_handler(request: Request, exc: AnalysisNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


@app.exception_handler(BaseAppException)
async def base_app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )


@app.get("/")
async def root():
    return {
        "message": "Document Versioning Service API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "POST /files/upload",
            "list": "GET /files",
            "analyze": "POST /files/{file_id}/analyze",
            "get_analysis": "GET /files/{file_id}/analysis"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
