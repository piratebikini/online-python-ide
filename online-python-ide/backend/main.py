from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    input_data: str = ""

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.post("/run")
def run_code(request: CodeRequest):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
            f.write(request.code.encode())
            file_path = f.name

        result = subprocess.run(
            ["python", file_path],
            input=request.input_data,
            text=True,
            capture_output=True,
            timeout=5
        )

        os.remove(file_path)

        return {
            "output": result.stdout,
            "error": result.stderr
        }

    except Exception as e:
        return {"error": str(e)}