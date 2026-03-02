from shlex import split, join

while s := input():
    cmd, *args = split(s)
    print(cmd, len(args), args)
