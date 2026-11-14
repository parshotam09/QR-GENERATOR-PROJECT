
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import qrcode
import base64
from io import BytesIO
from pathlib import Path

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent


class QRData(BaseModel):
    link: str



@app.get("/")
def home():
    return FileResponse(BASE_DIR / "template" / "index.html")



@app.post("/route")
def create_qr(data: QRData):

    img = qrcode.make(data.link)

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return {
        "qr_code": f"data:image/png;base64,{qr_base64}"
    }
