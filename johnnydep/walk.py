import json
from pathlib import Path

python_matches = ["requirements.txt", "requirements-dev.txt"]
node_matches = ["package.json"]

node_install = "npm install"

def walk(path:str="./"):
    pass

def node_license_walk(path:str="./node_modules/"):
    default_fields = [
        "name", 
        "summary", 
        "specifier", 
        "requires", 
        "required_by",
        "license"
    ]
    license = {}
    for p in Path(path).rglob('**/package.json'):
        # print(p)
        with open(p) as file:
            d=json.load(file)
            try:
                key=d["name"] + "@" + d["version"]
                if type(d["license"]) == type({}):
                    license[key]=d["license"]["type"]
                else:
                    license[key]=d["license"]
            except:
                pass
    print(json.dumps(license, indent=4))