from shlex import split, join

s1 = split(input())
s1 = ['register', join(s1[:3]), join(s1[3:])]
print(join(s1))
