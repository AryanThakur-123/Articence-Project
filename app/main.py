
from fastapi import FastAPI
from app.routers import health, data, llm, llm_executor
from app.utils.logging import configure_logging


configure_logging()

app = FastAPI(title="Universal Data Connector")

app.include_router(health.router)
app.include_router(data.router)
app.include_router(llm.router)
app.include_router(llm_executor.router)
