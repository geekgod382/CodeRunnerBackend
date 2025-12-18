# Code Runner Backend 🔧

A lightweight FastAPI-based backend for Code Editor project that accepts code in multiple languages (C, C++, Java), compiles and runs it in an isolated docker container , and returns the program output.

---

## Features ✅

- Single HTTP endpoint to run code: POST `/run`
- Language runners for: **C**, **C++**, and **Java**
- Runs code in a temporary directory in a container and returns stdout
- Dockerized for easy local deployment

---

## Quick Start 🚀

Requirements:

- Python 3
- System compilers / runtimes: `gcc`, `g++`, `javac`, and `java`

Install Python dependencies and run locally:

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`.

---

## Docker 🐳

Build the image:

```bash
docker build -t code-runner-backend:latest .
```

Run the container:

```bash
docker run --rm -p 8000:8000 code-runner-backend:latest
```

The Dockerfile installs system compilers (`gcc`, `g++`, `openjdk`) so the container can compile and run submitted programs.

---

## Project Structure 🗂️

```
app.py                 # FastAPI app and /run endpoint
requirements.txt       # Python dependencies
Dockerfile             # Docker image build
runners/
  c_runner.py         # Compile & run C code (gcc)
  cpp_runner.py       # Compile & run C++ code (g++)
  java_runner.py      # Compile & run Java code (javac & java)
```

Each runner writes the submitted source to a temporary directory, compiles it when needed, runs it, and returns stdout.

---

## Extending / Adding Languages 🔧

To add a new language:

1. Create a new runner module under `runners/`, e.g., `python_runner.py` with a function `run_python(code, tmp)` that returns `{'output': ...}` or `{'error': ...}`.
2. Import and wire it into `app.py`'s `run_code` handler.
3. Add any required system dependencies to the `Dockerfile`.

---
