from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from extractor.api.routes import router as api_router

app = FastAPI(
    title="Bore Log Transformer Extraction API",
    description="Automated document extraction service for geological and geotechnical bore logs using Vision Transformers.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def root():
    return {
        "name": "Bore Log Extractor Engine",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }
