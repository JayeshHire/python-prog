import io
import os

class HttpHandler:

    def __init__(self, request, response: io.BytesIO):
        self.request = request.decode()
        self.response = response
        self.file_path = os.path.join(os.getcwd(), "static")
        self.files = [f for f in os.listdir(self.file_path) if os.path.isfile(f)]
        self.resolver()
        
        method_call = getattr(self, f"handle_{self.method}")
        method_call()

    def resolver(self):
        line = self.request.split("\r\n")[0]
        line_data = line.split(" ")
        self.method = line_data[0]
        self.path = line_data[1]
        self.protocol = line_data[2]
    
    def handle_GET(self):
        body =  ""
        f = ""
        if self.path == "/":
            f = "index.html"
            f = os.path.join(self.file_path, f)
            self.status = "200 OK"
        else :
            f = self.path.lstrip("/")
            f = os.path.join(self.file_path, f)
            if f not in self.files:
                self.status = "404 Not Found"
            else:
                self.status = "200 OK"

        self.content_type = "text/html"
        if self.status == "404 Not Found":
            body = "<h1>Not found</h1>"
        elif self.status == "200 OK":
            with open(f, "r") as file:
                body = file.read()
        
        packet = (
            f"{self.protocol} {self.status}\r\n"
            f"Content-Type: {self.content_type}\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{body}"
        )
        self.response.write(packet.encode("utf-8"))
        pass 

    def handle_PUT(self):
        pass 

    def handle_POST(self):
        pass 

    def handle_DELETE(self):
        pass 

