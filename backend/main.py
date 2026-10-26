from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import account, auth
from app.core.database import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="BuildLog API",
    description="공부 기록, 할 일, 오류 해결 방법을 한곳에 모아두는 웹사이트 API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS 설정 - React 개발 서버와 통신 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(account.router)


@app.get("/")
def read_root():
    return {"message": "BuildLog API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
