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
    data = zlib.decompress(Path(repo + '/.git/objects/' + text[:2] + '/' + text[2:]).read_bytes()).decode()
    text2 = data.split('tree')[1].split()[0]
    header, _, body = zlib.decompress(Path(repo + '/.git/objects/' + text2[:2] + '/' + text2[2:]).read_bytes()).partition(b'\x00')
    kind, size = header.split()
    print('TREE for commit', text)
    while body:
        treeobj, _, body = body.partition(b'\x00')
        tmode, tname = treeobj.split()
        num, body = body[:20], body[20:]
        header2, _, body2 = zlib.decompress(Path(repo + '/.git/objects/' + str(num.hex())[:2] + '/' + str(num.hex())[2:]).read_bytes()).partition(b'\x00')
        kind2, size2 = header2.split()
        print(f'{kind2.decode()} {num.hex()}   {tname.decode()}')
    while 'parent' in data:
        text = data.split('parent')[1].split()[0]
        print('TREE for commit', text)
        data = zlib.decompress(Path(repo + '/.git/objects/' + text[:2] + '/' + text[2:]).read_bytes()).decode()
        text2 = data.split('tree')[1].split()[0]
        header, _, body = zlib.decompress(Path(repo + '/.git/objects/' + text2[:2] + '/' + text2[2:]).read_bytes()).partition(b'\x00')
        kind, size = header.split()
        while body:
            treeobj, _, body = body.partition(b'\x00')
            tmode, tname = treeobj.split()
            num, body = body[:20], body[20:]
            header2, _, body2 = zlib.decompress(Path(repo + '/.git/objects/' + str(num.hex())[:2] + '/' + str(num.hex())[2:]).read_bytes()).partition(b'\x00')
            kind2, size2 = header2.split()
            print(f'{kind2.decode()} {num.hex()}   {tname.decode()}')
