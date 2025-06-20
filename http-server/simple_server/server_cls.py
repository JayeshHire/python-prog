from collections import namedtuple
from http_method import HttpMethodEnum
from pydantic import BaseModel
import pickle

# PathMap = namedtuple("PathMap", ["path", "view_func", "http_method"])
class PathMap(BaseModel):
    path: str
    view_func: function
    http_method: HttpMethodEnum


"""
Class Server:
    This is a singleton class. 
    For running the server first an object of server class should be created.
    run method should be called on this class.

    attributes:
        - paths_map (list[PathMap]): contains a list of PathMap which give
        info on the path, a function associated with it and the method associated 
        with it.

"""
class Server:
    
    def __init__(self):
        self.pathspec = []
        self.load_pathspec()
    
    def create_pathspec(self, path: str, func_name: function, http_method: HttpMethodEnum) -> PathMap | None:
        new_pathspec = PathMap(path=path, view_func=func_name, http_method=http_method)
        if new_pathspec in self.pathspec:
            return None
        return new_pathspec
    
    def add_pathspec(self, pathspec: PathMap | None):
        if pathspec is not None:
            self.pathspec.append(pathspec)

    def run(self):
        """
        creates and bind a socket at the specified port and address.
        start listening to the incoming request. 
        Seperate the header and the body of the request.
        According to the request, respond to the request.
        """
        pass

    def stop(self):
        """
        Stop listening to the incoming request. 
        close the socket.
        persist the data.
        """
        self.dump_pathspec()
        pass

    def load_pathspec(self):
        with open("path_map.pickle", "rb") as f:
            self.pathspec = pickle.load(f)
    
    def dump_pathspec(self):
        with open("path_map.pickle", "wb") as f:
            pickle.dump(self.pathspec, f)
        