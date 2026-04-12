"""Client program."""

import sys
import socket
import shlex
import threading
import readline


def receive_messages(s):
    """Receive all messages."""
    while True:
        try:
            reply = s.recv(1024).rstrip().decode()
            print(f'\n{reply}\n{readline.get_line_buffer()}', end="", flush=True)
        except:
            break


username = sys.argv[1]
host = "localhost"
port = 1337

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    
    s.sendall((username + '\n').encode())

    response = s.recv(1024).decode().strip()
    if response == "DENIED":
        print("Username already taken")
        sys.exit(1)
    print(response)

    receive_thread = threading.Thread(target=receive_messages, args=(s,), daemon=True)
    receive_thread.start()
    # while msg := sys.stdin.buffer.readline():
    while True:
        try:
            # cmd = shlex.split(msg.decode())
            msg = input()
            cmd = shlex.split(msg)
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
                    # s.sendall(msg)
                    s.sendall((msg + '\n').encode())
                else:
                    s.sendall('Invalid arguements\n'.encode())
            elif len(cmd) == 2 and cmd[0] == 'attack':
                s.sendall((' '.join(cmd) + ' 10\n').encode())
            elif len(cmd) == 4 and cmd[0] == 'attack' and cmd[2] == 'with' and cmd[3] in ['sword', 'spear', 'axe']:
                if cmd[3] == 'sword':
                    s.sendall((' '.join(cmd[:2]) + ' 10\n').encode())
                elif cmd[3] == 'spear':
                    s.sendall((' '.join(cmd[:2]) + ' 15\n').encode())
                elif cmd[3] == 'axe':
                    s.sendall((' '.join(cmd[:2]) + ' 20\n').encode())
            elif len(cmd) == 2 and cmd[0] == 'sayall':
                s.sendall((msg + '\n').encode())
            elif len(cmd) >= 1 and cmd[0] in ['up', 'down', 'left', 'right', 'addmon', 'attack', 'sayall']:
                s.sendall('Invalid arguements\n'.encode())
            else:
                s.sendall('Invalid command\n'.encode())
        except KeyboardInterrupt:
            s.sendall('quit\n'.encode())
            break
        except EOFError:
            s.sendall('quit\n'.encode())
            break
