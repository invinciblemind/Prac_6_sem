import sys
sys.path.insert(0, '../mood')
sys.path.insert(0, '../mood/server')

try:
    import server
    print("Module loaded successfully")
    print("Functions:", [x for x in dir(server) if not x.startswith('_')])
except Exception as e:
    print(f"Error: {e}")
