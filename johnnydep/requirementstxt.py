
from johnnydep.lib import JohnnyDist


class Target:
    def __init__(self, name, version):
        self.url=name

def parseFile(args, filename="requirements.txt"):
    dists = []
    with open(filename) as file:
        for line in file:
            print(l:=line.rstrip())
            dists.append(JohnnyDist(
                    l,
                    index_url=args.index_url,
                    env=args.env,
                    extra_index_url=args.extra_index_url,
                    ignore_errors=args.ignore_errors,
                )
            )
    for idx, d in enumerate(dists):
        print("[")
        print(d.serialise(fields=args.fields, format="json", recurse=args.recurse))
        if idx < len(dists)-1:
            print(",")
        print("]")