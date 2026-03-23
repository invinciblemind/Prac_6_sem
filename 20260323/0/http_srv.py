import socket
import http.server

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(ip := s.getsockname()[0])
s.close()

http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler, bind=ip)
