import subprocess, os

def run_java(code, tmp):
    src = os.path.join(tmp, 'Main.java')

    open(src, 'w').write(code)
    subprocess.run(
        ['javac', src],
        stderr=subprocess.PIPE,
        check=True
    )

    out = subprocess.check_output(
        ['java', '-cp', tmp, 'Main'],
        stderr=subprocess.STDOUT,
        timeout=3
    )

    return {'output' : out.decode()}