from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
)

origins = [
    "http://localhost:3000",  # Local Next.js
    # "https://your-app.vercel.app",  # Deploy ke baad apna Vercel URL yahan add karna
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Backend Running 🚀",
    }