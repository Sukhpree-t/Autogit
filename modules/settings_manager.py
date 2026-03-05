
import os, json, platform

DEFAULT = {
    "username":"",
    "token":"",
    "repo_name":"",
    "repo_path":"",
    "commit_interval":5
}

def settings_path():
    if platform.system()=="Windows":
        base = os.getenv("APPDATA")
        folder = os.path.join(base,"autogit")
    else:
        home = os.path.expanduser("~")
        folder = os.path.join(home,".autogit")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder,"settings.json")

def load():
    path=settings_path()
    if not os.path.exists(path):
        with open(path,"w") as f:
            json.dump(DEFAULT,f,indent=4)
        return DEFAULT
    with open(path) as f:
        return json.load(f)

def save(data):
    with open(settings_path(),"w") as f:
        json.dump(data,f,indent=4)
