import sys
import os

args = sys.argv
repo = args[1]
if len(args) == 2:
    branches = os.listdir(repo + '/.git/refs/heads')
    print('\n'.join(branches))
