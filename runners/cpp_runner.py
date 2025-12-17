import subprocess, os

def run_cpp(code, tmp):
    src = os.path.join(tmp, 'main.cpp')
    exe = os.path.join(tmp, 'a.out')
    
    open(src, 'w').write(code)
    subprocess.run(
        ['g++', src, '-o', exe],
        stderr=subprocess.PIPE,
        check=True
    )

    out = subprocess.check_output(
        [exe],
        stderr=subprocess.STDOUT,
        timeout=3
    )

    return {'output' : out.decode()}