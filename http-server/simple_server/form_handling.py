import re
from abc import ABC, abstractmethod
import json


class UnsupportedMediaTypeException(Exception):
    def __init__(self, message):
        self.message = message
    
class OpSeqInvalidException(Exception):
    def __init__(self, message):
        self.message = message


class FormAbstract(ABC):

    @abstractmethod
    def submit(self):
        pass

    @abstractmethod
    def get_request_line(self):
        pass

    @abstractmethod
    def extract_header(self):
        pass 

    @abstractmethod
    def validate_content_type(self):
        pass 

    @abstractmethod
    def parse_data(self):
        pass 


class URLEncodedForm(FormAbstract):

        def __init__(self, request_body: str):
            self.request_body = request_body
            self.method = None
            self.path = None 
            self.protocol = None
            self.host = None 
            self.content_type = None
            self.content_length = None
            self.form_data = None 
            # self.get_request_line()
        
        def submit(self):
            self.get_request_line()
            self.extract_header()

            if self.validate_content_type():
                self.parse_data()
            else:
                raise UnsupportedMediaTypeException("Only url encoded form data can be handled.")

        def get_request_line(self):
            l1 = self.request_body.split("\r\n")[0].split(" ")
            self.method = l1[0]
            self.path = l1[1]
            self.protocol = l1[2]

        def extract_header(self):
            header_str = self.request_body.split("\r\n\r\n")[0]
            host_pattern = r"Host:\s*([a-zA-Z0-9\s/-:.]*)\r\n"
            content_type_pattern = r"Content-Type:\s*([a-zA-Z0-9-\s/]*)\r\n"
            content_length_pattern = r"Content-Length:\s*([0-9]*)\r\n"
            self.host = re.search(host_pattern, header_str, re.IGNORECASE).groups()[0]
            self.content_type = re.search(content_type_pattern, header_str, re.IGNORECASE).groups()[0]
            try:
                self.content_length = int(re.search(content_length_pattern, self.request_body, re.IGNORECASE).groups()[0])
            except ValueError:
                print("Some invalid value is given for content-length. Check form_handling.py, line 48")
                self.request_body = None
            except AttributeError:
                print("Some invalid value is given for content-length. Check form_handling.py, line 48")
                self.request_body = None
                
        def validate_content_type(self) -> bool:
            if self.content_type is None:
                raise OpSeqInvalidException("Incorrect call for validate_content_type function before extract_header function")
            
            if self.content_type == "application/x-www-form-urlencoded":
                return True
            else:
                return False
        
        def parse_data(self):
            d_ = re.search("\r\n\r\n(.*)", self.request_body).groups()[0]
            if self.content_length is None:
                raise OpSeqInvalidException("call extract_header and validate_content_type method first before calling parse_data ")
            
            if not self.validate_content_type():
                raise UnsupportedMediaTypeException(f"Content type should be 'application/x-www-form-urlencoded' but {self.content_type} was given")
            
            form_data = d_[0:self.content_length]

            def form_data_deserialize(fd: str) -> dict:
                key_vals = fd.split("&")
                fd_dict = { x.split("=")[0]: x.split("=")[1] for x in key_vals}
                return fd_dict
            
            self.form_data = form_data_deserialize(form_data)


class MultipartForm(FormAbstract):

    def __init__(self, request_body: str):
        self.request_body = request_body
        self.method = None
        self.path = None 
        self.protocol = None
        self.host = None 
        self.content_type = None
        self.form_data = None
        self.boundary = None

    def get_request_line(self):
        l1 = self.request_body.split("\r\n")[0].split(" ")
        self.method = l1[0]
        self.path = l1[1]
        self.protocol = l1[2]

    def extract_header(self):
        header_str = self.request_body.split("\r\n\r\n")[0]
        host_pattern = r"Host:\s*(.*)\r\n"
        content_type_pattern = r"Content-Type:\s*(.*)"
        boundary_pattern = r';boundary="(.*)"'
        content_type_val = re.search(content_type_pattern, header_str, re.IGNORECASE).groups()[0]
        self.boundary = re.search(boundary_pattern, content_type_val, re.IGNORECASE).groups()[0]
        self.host = re.search(host_pattern, header_str, re.IGNORECASE).groups()[0]
        self.content_type = re.search(r"(.*);", content_type_val, re.IGNORECASE).groups()[0]

    def validate_content_type(self):
        if self.content_type is None:
            raise OpSeqInvalidException("Incorrect call for validate_content_type function before extract_header function")

        if self.content_type == "multipart/form-data":
            return True
        else:
            return False

    def parse_data(self):
        if not self.validate_content_type():
            raise UnsupportedMediaTypeException(f"content type should be 'multipart/form-data' but {self.content_type} was given")
        
        pat = fr"(--{self.boundary}\r\n.*\r\n\r\n.*\r\n)"
        cd_pat = fr'--{self.boundary}\r\ncontent-disposition:\s*(.*\r\n\r\n.*)\r\n'
        f_data = re.findall(pat, self.request_body, re.IGNORECASE)
        content_dispositions = [
            re.search(cd_pat, d, re.IGNORECASE).groups()[0]
            for d in f_data
        ]

        fields = []
        for cd in content_dispositions:
            val_header = cd.split("\r\n\r\n")
            cd_lst = val_header[0].split(";")
            dispo_val = cd_lst[0]
            if dispo_val.strip() == "form-data":
                a = [x for x in cd_lst if re.search(r"\s+name=(.*)", x) is None]
                field_name = [x for x in cd_lst if re.search(r"\s+name=(.*)", x) is not None]
                field_name = field_name[0].split("=")[1].strip('"')
                attrs = {attr.split("=")[0].strip(): attr.split("=")[1].strip('"') for attr in a[1::] }
                field_value = val_header[1]
                fields.append(
                        {
                            "name": field_name,
                            "value": field_value,
                            "attrs": attrs
                        }
                    )

        self.form_data = fields

    def submit(self):
        self.get_request_line()
        self.extract_header()
        self.parse_data()


class JSONDataHandling(FormAbstract):

    def __init__(self, request_body: str):
        self.request_body = request_body
        self.method = None
        self.path = None 
        self.protocol = None
        self.host = None 
        self.content_type = None
        self.content_length = None
        self.json_data = None 
        pass

    def get_request_line(self):
        l1 = self.request_body.split("\r\n")[0].split(" ")
        self.method = l1[0]
        self.path = l1[1]
        self.protocol = l1[2]

    def extract_header(self):
        header_str = self.request_body.split("\r\n\r\n")[0]
        host_pat = r"Host:\s*(.*)\r\n"
        content_type_pattern = r"Content-Type:\s*(.*)\r\n"
        content_length_pattern = r"Content-Length:\s*([0-9]*)"
        self.host = re.search(host_pat, header_str, re.IGNORECASE).groups()[0]
        self.content_type = re.search(content_type_pattern, header_str, re.IGNORECASE).groups()[0]
        self.content_length = int(re.search(content_length_pattern, header_str, re.IGNORECASE).groups()[0])
        pass

    def validate_content_type(self):
        if self.content_type is None:
                raise OpSeqInvalidException("Incorrect call for validate_content_type function before extract_header function")
        
        if self.content_type == "application/json":
            return True
        else:
            return False
    
    def parse_data(self):
        if self.validate_content_type():
            data_str = self.request_body.split("\r\n\r\n")[1]
            self.json_data = json.loads(data_str)
        else:
            raise UnsupportedMediaTypeException(f"content type should be 'application/json' but {self.content_type} was given")

    def submit(self):
        self.get_request_line()
        self.extract_header()
        if self.content_length is None:
                raise OpSeqInvalidException("call extract_header and validate_content_type method first before calling parse_data ")
        
        if self.validate_content_type():
            self.parse_data()
        else:
            raise UnsupportedMediaTypeException(f"Content type should be 'application/json' but {self.content_type} was given")