import sys
import socket
import cmd 
from pathlib import Path
from shlex import split
import readline
'''
host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    while msg := sys.stdin.buffer.readline():
        s.sendall(msg)
        print(s.recv(1024).rstrip().decode())
'''
class CliSrv(cmd.Cmd):
    prompt = f"{Path.cwd()}> "
    
    def __init__(self, s):
        super().__init__()
        self.s = s
    
    def do_print(self, arg):
        """print something"""
        self.s.sendall(('print ' + arg + '\n').encode())
        print(s.recv(1024).rstrip().decode())

    def do_info(self, arg):
        """show port/host"""
        self.s.sendall(('info ' + arg + '\n').encode())
        print(s.recv(1024).rstrip().decode())

    def complete_info(self, text, line, begidx, endidx):
        if len((line + '.').split()) == 2:
            return [arg for arg in ['host', 'port'] if arg.startswith(text)]

    def do_EOF(self, arg):
        return -1

if __name__ == "__main__":
    readline.set_completer_delims('" ')
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    CliSrv(s).cmdloop()
