from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(title="Platonov CV")

STATIC = Path(__file__).parent / "static"

app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/")
async def index():
    return FileResponse(STATIC / "index.html")


@app.get("/box-measurement")
async def box_measurement():
    return FileResponse(STATIC / "box-measurement.html")


@app.get("/bill-parser")
async def bill_parser():
    return FileResponse(STATIC / "bill-parser.html")


@app.get("/fpv-tricks")
async def fpv_tricks():
    return FileResponse(STATIC / "fpv-tricks.html")
