import os, sys, subprocess, platform

VENV = ".venv"
MAIN = "main_gui.py"

def python_in_venv():
    if platform.system()=="Windows":
        return os.path.join(VENV,"Scripts","python")
    return os.path.join(VENV,"bin","python")

def pip_in_venv():
    if platform.system()=="Windows":
        return os.path.join(VENV,"Scripts","pip")
    return os.path.join(VENV,"bin","pip")

def create_env():
    print("Creating virtual environment...")
    subprocess.check_call([sys.executable,"-m","venv",VENV])

def install():
    pip = pip_in_venv()
    subprocess.check_call([pip,"install","--upgrade","pip"])
    subprocess.check_call([pip,"install","-r","requirements.txt"])

def run():
    subprocess.check_call([python_in_venv(), MAIN])

if __name__=="__main__":
    if not os.path.exists(VENV):
        create_env()
        install()
    run()
