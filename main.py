import logging
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.api_routes import router as api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Vibe BPMN")
app.include_router(api_router, prefix="/api")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/health")
async def health():
    logger.info("Health check successful")
    return {"status": "OK"}


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")
