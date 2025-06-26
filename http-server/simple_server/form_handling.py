import re
from abc import ABC, abstractmethod


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
    def get_form_data(self):
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
                self.get_form_data()
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
        
        def get_form_data(self):
            d_ = re.search("\r\n\r\n(.*)", self.request_body).groups()[0]
            if self.content_length is None:
                raise OpSeqInvalidException("call extract_header and validate_content_type method first before calling get_form_data ")
            
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
        content_type_pattern = r"Content-Type:\s*(.*)\r\n"
        boundary_pattern = r';boundary="(.*)";|\r\n'
        content_type_val = re.search(host_pattern, self.request_body, re.IGNORECASE).groups()[0]
        self.boundary = re.search(boundary_pattern, content_type_val, re.IGNORECASE).groups()[0]
        self.host = re.search(host_pattern, self.request_body, re.IGNORECASE).groups()[0]
        self.content_type = re.search(r"(.*);", content_type_val, re.IGNORECASE).groups()[0]

    def validate_content_type(self):
        if self.content_type is None:
            raise OpSeqInvalidException("Incorrect call for validate_content_type function before extract_header function")

        if self.content_type == "multipart/form-data":
            return True
        else:
            return False

    def get_form_data(self):
        pat = fr"\r\n(--{self.boundary}\r\n.*\r\n\r\n.*\r\n--{self.boundary}--)"
        cd_pat = fr'--{self.boundary}\r\ncontent-disposition:\s*(.*\r\n\r\n.*)\r\n--{self.boundary}'
        cd_val_pat = "(.*);.*"
        cd_name_pat = '.*;name="(.*)"'
        field_val_pat = '\r\n\r\n(.*)'
        f_data = re.search(pat, self.request_body, re.IGNORECASE).groups()[0]
        
        content_dispositions = re.search(cd_pat, f_data, re.IGNORECASE).groups()

        fields = {}
        for cd in content_dispositions:
            cd_val = re.search(cd_val_pat, cd, re.IGNORECASE).groups()[0]
            if cd_val.strip() == "form-data":
                field_name = re.search(cd_name_pat, cd, re.IGNORECASE).groups()[0]
                field_val = re.search(field_val_pat, cd, re.IGNORECASE).groups()[0]
            fields[field_name] = field_val
        return fields

    def submit(self):
        pass