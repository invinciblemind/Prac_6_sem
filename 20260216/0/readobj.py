from pathlib import Path
import zlib
import sys

'''
data = zlib.decompress(Path(sys.argv[1]).read_bytes())
print(data)
'''

'''
for obj in Path(sys.argv[1]).glob('.git/objects/??/*'):
    print(obj)
'''

objs = []
for obj in Path(sys.argv[1]).glob('.git/objects/??/*'):
    head, _, body = zlib.decompress(obj.read_bytes()).partition(b'\x00')
    typ = head.decode().split()[0]
    if typ == 'commit':
        print(body.decode())
        objs.append(obj)
for obj in objs:
    print(obj)
