import socket
import sys


def sqroots(coeffs:str) -> str:
    a, b, c = map(int, coeffs.split())
    D = b * b - 4 * a * c
    if D / (a ** 2) < 0:
        return ''
    elif D == 0:
        return str(-b / (2 * a))
    else:
        return f'{(-b + D ** 0.5) / (2 * a)} {(-b - D ** 0.5) / (2 * a)}'


def sqrootnet(coeffs: str, s: socket.socket) -> str:
    s.sendall((coeffs + "\n").encode())
    return s.recv(128).decode().strip()


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 1337))
        s.sendall(sys.argv[1].encode() + b'\n')
        print(s.recv(1024).rstrip().decode())
