"""Optional FastAPI serving precomputed data."""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="Key Person Risk Index API", version="0.1.0")
DATA = Path("docs/data")

@app.get("/sectors")
def sectors():
    p = DATA / "kpri.json"
    if not p.exists():
        return {"error": "Run make all first"}
    return json.loads(p.read_text())

@app.get("/events")
def events():
    p = DATA / "events.csv"
    if not p.exists():
        return {"error": "No events"}
    return FileResponse(p, media_type="text/csv")

@app.get("/index")
def index():
    return {"message": "KPRI API", "docs": "/docs"}
