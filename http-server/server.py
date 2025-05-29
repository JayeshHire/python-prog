import socket 
import logging
import io
from http_handler import HttpHandler

logger = logging.getLogger(__name__)


HOST = '127.0.0.1'
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Listening on {HOST}:{PORT}')
    conn, addr = s.accept()
    with conn:
        print(f'Connected to {addr}')
        # while True:
        request = conn.recv(4028)
        # print(data)
        
        body = "Hello world"
        response = io.BytesIO()
        handler = HttpHandler(request, response)

        data = response.getvalue()
        conn.sendall(data)
        print("data sent successfully")