from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.tasks import router as task_router

app = FastAPI(title="DeliveryFlow Tasks API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
