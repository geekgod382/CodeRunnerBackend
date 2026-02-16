from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess, tempfile, os, uuid
from runners.c_runner import run_c
from runners.cpp_runner import run_cpp
from runners.java_runner import run_java
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from jose import jwt
import os

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

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

async def verify_token(authorization : str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# Mount the static directory for serving CSS, JS, images, etc.
app.mount('/static', StaticFiles(directory=STATIC_DIR), name="static")
@app.get('/', response_class=FileResponse)
def serve_index():
    index_path = os.path.join(STATIC_DIR, "home.html")
    if not os.path.exists(index_path):
        return {"error": "home.html not found"}
    return FileResponse(index_path)

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
        

# for testing only
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)