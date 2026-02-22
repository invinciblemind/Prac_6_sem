from pathlib import Path
import zlib
import sys
import os

args = sys.argv
repo = args[1]
if len(args) == 2:
    branches = os.listdir(repo + '/.git/refs/heads')
    print('\n'.join(branches))
else:
    branch = args[2]
    f = open(repo + '/.git/refs/heads/' + branch)
    text = f.readline()[:-1]
    data = zlib.decompress(Path(repo + '/.git/objects/' + text[:2] + '/' + text[2:]).read_bytes())
    print(data.decode())
