import os
from pathlib import Path

# file_name = os.path.join(os.getcwd(), "static", "index.html")
# p = Path(os.getcwd())

# print([f for f in p.iterdir()])
# print(Path(file_name).is_file())

class Name: 
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def get_a(self):
        print("getting value of a")

    def get_b(self):
        print("getting value of b")

name = Name("jay", "sam")

v = getattr(name, "get_a")
v()