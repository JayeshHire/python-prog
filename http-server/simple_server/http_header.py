from pydantic import BaseModel
from dataclasses import dataclass
from enum import Enum
import copy


# @dataclass
class HttpHeaderModel(BaseModel):
    method: str
    path: str 
    protocol: str 
    header_dict: dict


class HttpHeaderType(Enum):
    REQUEST_HEADER = 1
    RESPONSE_HEADER = 2


@dataclass
class HttpRequestLine:
    method: str
    path: str
    protocol: str


@dataclass
class HttpHeaderFieldAttr:
    name: str
    value: str


@dataclass
class HttpHeaderField:
    field: str
    values: list[str] | str
    attrs: list[HttpHeaderFieldAttr] | None


class HttpHeader:
    """
    header_unserialized: it is expected to have no \r\n at the end

    attr:
        - method
        - path
        - protocol
        - header_str
        - header_deserialized
    """
    def __init__(self, header_serialized: str | None = None, header_type: HttpHeaderType | None = None, header_deserialized: list[HttpHeaderField] | None= None):
        self.header_serialized = header_serialized
        self.header_deserialized = header_deserialized
        self.request_line = None
        self.response_line = None
        self.header_type = header_type
        # self.serialize()
        # self.deserialize()
    
    def deserialize(self) -> None:
        if self.header_serialized is not None:
            lines = self.header_serialized.split("\r\n")
            line1 = lines[0].split(" ")
            method = line1[0].strip()
            path = line1[1].strip()
            protocol = line1[2].strip()
            self.request_line = HttpRequestLine(method, path, protocol)
            self.header_deserialized = HttpHeader.header_keyval_deserialize(lines[1::])
        
    def serialize(self) -> None:
        if self.header_deserialized is not None:
            # self.header_str = dict2str(self.header_dict)
            header_serialize = ""
            if self.header_type == HttpHeaderType.REQUEST_HEADER:
                header_serialize += f"{self.request_line}\r\n"
            elif self.header_type == HttpHeaderType.RESPONSE_HEADER:
                header_serialize += f"{self.response_line}\r\n"
            for header in self.header_deserialized:
                attrs = [f";{attr.name}={attr.value}" for attr in header.attrs] 
                tmp_header = f"{header.field}: {header.values}{attrs}\r\n"
                header_serialize += tmp_header

            self.header_serialized = header_serialize + "\r\n"
        
    @classmethod
    def header_keyval_deserialize(cls, header_keyvals: list[str]) -> list[HttpHeaderField]:
        keyval_deserialize = [HttpHeader.parse_header(key_val) for key_val in header_keyvals]
        return keyval_deserialize
    
    @classmethod
    def parse_header(cls, header_str: str = None):
        # header_str = "User-Agent: Mozilla/5.0 , Google, Safari (Macintosh; Intel Mac OS X 10.9; rv:50.0) ; Gecko=20100101 ; Firefox=50.0 (hii)"
        field = header_str.split(":")[0]

        val_str = ":".join(header_str.split(":")[1::])
        attrs = val_str.split(";")

        new_attrs_lst = []

        new_attr = ""

        i = 0
        while i < len(attrs):
            if "(" in attrs[i] and ")" not in attrs[i]:
                temp_i = i
                new_attr += attrs[i]
                i += 1
                while ")" not in attrs[i] :
                    new_attr += ";" + attrs[i]
                    i += 1
                new_attr += ";" + attrs[i]
                i += 1
                new_attrs_lst.append(new_attr)
                new_attr = ""
                continue 
            new_attrs_lst.append(attrs[i])
            i += 1

        values = new_attrs_lst[0].split(",")
        attrs = [HttpHeaderFieldAttr(attr.split("=")[0], attr.split("=")[1]) for attr in new_attrs_lst[1::]]
        header_deserialized = HttpHeaderField(field, values, attrs)
        return header_deserialized
    
    def __str__(self):
        return f"HttpHeader (\
            request-line: {self.request_line},\
            response-line: {self.response_line},\
            serialized: {self.header_serialized},\
            deserialized: {self.header_deserialized},\
            header-type: {self.header_type}\
                )"