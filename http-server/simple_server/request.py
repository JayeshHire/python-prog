import copy

class Form:
    def __init__(self, *args, **kwargs):
        pass


class FormFieldBody:
    def __init__(self, field_header: str):
        self.field_header = field_header
    
    def deserialize(self):
        header, value = self.field_header.split("\r\n\r\n")
        self.header = HttpHeader(header)
        _, *header_attrs = self.header.header_dict["Content-Disposition"].split(";")
        header_attrs = {attr.split("=")[0].strip(): attr.split("=")[1].strip() for attr in header_attrs}
        field = header_attrs["name"]
        filename = None
        if self.header.header_dict.get("Content-Type", None) == "text/plain":
            filename = header_attrs["filename"]
            

class Request:
    def __init__(self, content: bytes):
        self.request_content = content.decode("utf-8")
    
    """
    Function:
        name: deserialize
        description: converts string into python objects
    """
    def deserialize(self):
        header_content, body_content = self.request_content.split("\r\n\r\n")
        self.http_header = HttpHeader(header_serialized=header_content)
        if self.http_header.method == "GET" :
            self.body = None 
        elif self.http_header.method == "PUT" or self.http_header.method == "POST":
            self.body = body_deserialize(body_content)
        
        def body_deserialize(body: str):
            """
            Content-Type: 
                - multipart/form-data
                - application/x-www-form-urlencoded
                - application/json
                - text/html
                - text/javascript
                - text/css
            
            description: converts string to python object
            """

            def multipart_form_handler(body: str):
                media_type, *attrs = self.http_header.header_dict["Content-Type"].split(";")
                media_type = media_type.strip()
                attrs = { attr.split("=")[0].strip(): attr.split("=")[1].strip() for attr in attrs}
                boundary_string = attrs["boundary"]
                # requires a form class to store form data.

                form_field_info = list(
                    filter(
                        lambda x: x != "", body.split(f"--{boundary_string}\r\n")
                    )
                )
                

                def header_filter(header_serialized: str):

                    pass

            def url_encoded_form_handler(body: str):
                pass 

            def json_handler(body: str):
                pass 
            

# can handle GET request
