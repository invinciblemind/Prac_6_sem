import sys
import socket
import shlex

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    while msg := sys.stdin.buffer.readline():
        cmd = shlex.split(msg.decode())
        if len(cmd) == 1 and len(cmd[0]) <= 5:
            if cmd[0] == 'up':
                s.sendall('move 0 -1\n'.encode())
            elif cmd[0] == 'down':
                s.sendall('move 0 1\n'.encode())
            elif cmd[0] == 'left':
                s.sendall('move -1 0\n'.encode())
            elif cmd[0] == 'right':
                s.sendall('move 1 0\n'.encode())
            else:
                s.sendall('Invalid command\n'.encode())
        elif len(cmd) == 9 and cmd[0] == 'addmon':
            name = cmd[1]
            hello_str = cmd[cmd.index('hello') + 1]
            hp = cmd[cmd.index('hp') + 1]
            xx, yy = cmd[cmd.index('coords') + 1:cmd.index('coords') + 3]
            if xx.isdigit() and yy.isdigit() and 0 <= int(xx) <= 9 and 0 <= int(yy) <= 9:
                s.sendall(msg)
            else:
                s.sendall('Invalid arguements\n'.encode())
        elif len(cmd) == 2 and cmd[0] == 'attack':
            s.sendall((' '.join(cmd) + ' 10\n').encode())
        elif len(cmd) == 4 and cmd[0] == 'attack' and cmd[2] == 'with' and cmd[3] in ['sword', 'spear', 'axe']:
            if cmd[3] == 'sword':
                s.sendall((' '.join(cmd) + ' 10\n').encode())
            elif cmd[3] == 'spear':
                s.sendall((' '.join(cmd) + ' 15\n').encode())
            elif cmd[3] == 'axe':
                s.sendall((' '.join(cmd) + ' 20\n').encode())
        elif len(cmd) >= 1 and cmd[0] in ['up', 'down', 'left', 'right', 'addmon', 'attack']:
            s.sendall('Invalid arguements\n'.encode())
        else:
            s.sendall('Invalid command\n'.encode())
        print(s.recv(1024).rstrip().decode())
