from fastapi import FastAPI
from pydantic import BaseModel
import subprocess, tempfile, os, uuid
from runners.c_runner import run_c
from runners.cpp_runner import run_cpp
from runners.java_runner import run_java
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class Code(BaseModel):
    language : str
    code : str

TIMEOUT = 3

@app.post('/run')
def run_code(payload : Code):
    lang, code = payload.language, payload.code
    with tempfile.TemporaryDirectory() as tmp:
        try:
            if lang == "c":
                return run_c(code, tmp)
            elif lang == 'cpp':
                return run_cpp(code, tmp)
            elif lang == 'java':
                return run_java(code, tmp)
            else:
                return {'error' : 'Unsupported language'}
            
        except subprocess.TimeoutExpired:
            return {'error' : 'Execution timed out'}
        except Exception as e:
            return {'error' : str(e)}