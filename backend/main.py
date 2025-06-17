from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import shutil
from pathlib import Path
from backend import model_loader  # import your model logic
from fastapi import FastAPI, UploadFile, File
import os
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# Set up templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Ensure temp directory exists
    os.makedirs("temp", exist_ok=True)

    upload_path = f"temp/{file.filename}"

    try:
        with open(upload_path, "wb") as f:
            content = await file.read()
            f.write(content)

        predictions = model_loader.predict(upload_path)

        return {"predictions": predictions}

    except Exception as e:
        return {"error": str(e)}