import asyncio
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.get_base_diagram import get_base_diagramm

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="index.html")


@app.post("/api/generate")
async def generate_bpmn():
    """
    Generate BPMN XML code to render with bpmn-js
    """


@app.get("/api/base-bpmn-xml")
async def get_base_bpmn_xml():
    """
    Get the base BPMN XML structure
    """
    xml = asyncio.to_thread(get_base_diagramm())
    return {"xml": xml}
