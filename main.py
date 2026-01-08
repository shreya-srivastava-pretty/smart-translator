from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/interpret-signboard")
async def interpret_signboard(
    file: UploadFile,
    lang: str = Form(...)
):
    return {
        "message": f"Received file {file.filename}",
        "language": lang
    }
