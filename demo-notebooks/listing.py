from ipywidgets import HTML

def listing(filename):
    width = len(filename) + 10
    print(f"{width*'-'}")
    header = f"file {filename}"
    print(f"{header:^{width}}")
    print(f"{width*'-'}")
    with open(filename) as code:
        for lineno, line in enumerate(code, 1):
            print(f"{lineno:02d}:{line}", end="")    