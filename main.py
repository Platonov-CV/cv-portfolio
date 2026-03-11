import os

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="Platonov CV")

FPV_BASE = os.getenv("FPV_SERVICE_URL", "http://fpv-trick-detection:8000")
BOX_BASE = os.getenv("BOX_SERVICE_URL", "http://box-measurement:8000")

STATIC = Path(__file__).parent / "static"
IMAGES = Path(__file__).parent / "images"

app.mount("/static", StaticFiles(directory=STATIC), name="static")
app.mount("/images", StaticFiles(directory=IMAGES), name="images")


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


@app.post("/fpv/process_video/")
async def fpv_process_video(request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{FPV_BASE}/process_video/",
            content=body,
            headers={"content-type": request.headers.get("content-type", "")},
            params=dict(request.query_params),
            timeout=60.0,
        )
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type=resp.headers.get("content-type"))


@app.get("/fpv/process_video/{job_id}/progress")
async def fpv_progress(job_id: str):
    async def stream():
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", f"{FPV_BASE}/process_video/{job_id}/progress",
                                     timeout=None) as resp:
                async for chunk in resp.aiter_bytes():
                    yield chunk

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.get("/fpv/process_video/{job_id}/result")
async def fpv_result(job_id: str):
    async def stream():
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", f"{FPV_BASE}/process_video/{job_id}/result",
                                     timeout=120.0) as resp:
                async for chunk in resp.aiter_bytes():
                    yield chunk

    return StreamingResponse(stream(), media_type="video/mp4")


@app.post("/box/process_frame/")
async def box_process_frame(request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BOX_BASE}/process_frame/",
            content=body,
            headers={"content-type": request.headers.get("content-type", "")},
            timeout=30.0,
        )
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type=resp.headers.get("content-type"))
