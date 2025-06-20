from pydantic import BaseModel
import copy

# class HeaderKeyVal(BaseModel):
class HttpHeaderModel(BaseModel):
    method: str
    path: str 
    protocol: str 
    header_dict: dict


class HttpHeader:
    """
    header_unserialized: it is expected to have no \r\n at the end

    attr:
        - method
        - path
        - protocol
        - header_str
        - header_dict
    """
    def __init__(self, header_serialized: str | None = None, header_dict: dict | None = None):
        self.header_str = header_serialized
        self.header_dict = header_dict
        self.serialize()
        self.deserialize()
    
    def deserialize(self) -> None:
        if self.header_str is not None:
            lines = self.header_str.split("\r\n")
            line1 = lines[0].split(" ")
            self.method = line1[0].strip()
            self.path = line1[1].strip()
            self.protocol = line1[2].strip()
            self.header_dict = str2dict(lines)
            lines = "\r\n".join(lines[1::])
            # self.header_dict = 
        """
        Function:
            Name: str_dict
            parameter: 
                - content(list[str])
            return:
                - dict
            
            description: 
                Takes a list of lines from the header and converts them into python dictionary.
        """
        def str2dict(header_lines: list[str]) -> dict:
            content_dict = {}
            key_val_lines = copy.deepcopy(header_lines)

            if ":" not in header_lines[0]:
                key_val_lines = key_val_lines[1::]
            
            key_val_lst = [[key_val.split(":")[0].strip(" "), 
                            key_val.split(":")[1].strip(" ")] 
                            for key_val in key_val_lines]
            
            for key, val in key_val_lst:
                content_dict[key] = val
            return content_dict
        
    def serialize(self) -> None:
        if self.header_dict is not None:
            self.header_str = dict2str(self.header_dict)

        """
        Function: 
            Name: dict2str
            parameter: 
                - header_dict(dict)
            return:
                - str (the output string contains \r\n at the end of every line 
                and \r\n\r\n at the end of the header)
            
            description:
                Converts the header dictionary to the header string
        """

        def dict2str(header_dict: dict) -> str:
            header_str = ""
            for key, val in header_dict.items():
                header_str += f"{key}: {val}\r\n"

            header_str+= "\r\n"
            return header_str
        
    @classmethod
    def header_keyval_deserialize(cls, header_keyvals: str) -> dict:
        keyvals_dict = {keyval.split(":")[0]: keyval.split(":")[1] for keyval in header_keyvals}
        keyval_attrs = {key : 
                            {
                                "value": val.split(";")[0],
                                "attr":{
                                attr.split("=")[0]: attr.split("=")[1].split(",") 
                                if "," in  attr.split("=")[1] else attr.split("=")[1]
                                for attr in val.split(";")[1::]
                                }    
                            }
                        for key, val in keyvals_dict.items()
                        }
        return keyval_attrs