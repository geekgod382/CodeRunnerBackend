import subprocess, os
from .mem_limit import memory_limit

def run_c(code, tmp):
    src = os.path.join(tmp, 'main.c')
    exe = os.path.join(tmp, 'a.out')
    
    open(src, 'w').write(code)
    try:
        compile_proc = subprocess.run(
            ["gcc", src, "-o", exe],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        if compile_proc.returncode != 0:
            return {"error": compile_proc.stderr.decode()}

    except subprocess.TimeoutExpired:
        return {"error": "Compilation Time Limit Exceeded"}

    try:
        run_proc = subprocess.run(
            [exe],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            preexec_fn=memory_limit
        )

        if run_proc.returncode != 0:
            return {"error": run_proc.stderr.decode()}

        return {"output": run_proc.stdout.decode()}

    except subprocess.TimeoutExpired:
        return {"error": "Time Limit Exceeded"}