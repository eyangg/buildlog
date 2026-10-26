from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BuildLog API",
    description="Multi-user study notes and task management API",
    version="0.1.0"
)

# CORS middleware configuration for React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "BuildLog API",
        "version": "0.1.0",
        "docs": "/docs",
        "openapi_schema": "/openapi.json"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
