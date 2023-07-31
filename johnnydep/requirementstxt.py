import json
from lib import JohnnyDist
from lib import flatten_deps

class Target:
    def __init__(self, name, version):
        self.url=name

def parseFile(args, filename="requirements.txt", ret=False):
    dists = []
    default_fields = [
        "name", 
        "summary", 
        "specifier", 
        "requires", 
        "required_by",
        "license"
    ]
    with open(filename) as file:
        for line in file:
            if line.find("#") >=0:
                line=line[0:line.find("#")]
            l=line.rstrip()
            if l[0:2] == '--' or not l:
                pass
            else:
                dists.append(JohnnyDist(
                        l,
                        index_url=args.index_url,
                        env=args.env,
                        extra_index_url=args.extra_index_url,
                        ignore_errors=args.ignore_errors,
                    )
                )
    data=[]
    for idx, d in enumerate(dists):
        deps=flatten_deps(d)
        data += deps
    output = [d for dep in data for d in dep.serialise(fields=default_fields, recurse=False)]
    dup_check = {}
    for idx, o in enumerate(output):
        k=o["name"]+o["specifier"]
        if k in dup_check:
            output[dup_check[k]]["required_by"].append(k)
            output.remove(o)
        else:
            dup_check[k] = idx

    result = json.dumps(output, indent=2, default=str, separators=(",", ": "))
    if not ret:
        print(result)
    else:
        return output