# contains all the headers that are supported
# name of the header attributes
# check if the header value is valid
# check if the header attribute and it's value is valid
# Error handling :
    # 1. Exception for invalid header field
    # 2. Exception for invalid header value
    # 3. Exception for invalid header attribute and it's value


# create a way to store all the headers that are supported along with their regex
# create a method for them to extract field, value and attribute for these fields.

from enum import Enum
import re
from pydantic.dataclasses import dataclass 


class HeaderType(Enum):
    REQUEST_HEADER = 0
    RESPONSE_HEADER = 1

class RequestHeader(Enum):
    # General Headers
    HOST = "Host"
    USER_AGENT = "User-Agent"
    ACCEPT = "Accept"
    ACCEPT_LANGUAGE = "Accept-Language"
    ACCEPT_ENCODING = "Accept-Encoding"
    CONNECTION = "Connection"
    REFERER = "Referer"
    ORIGIN = "Origin"
    CONTENT_LENGTH = "Content-Length"
    CONTENT_TYPE = "Content-Type"

    # Authentication Headers
    AUTHORIZATION = "Authorization"
    COOKIE = "Cookie"

    # Conditional Request Headers
    IF_MODIFIED_SINCE = "If-Modified-Since"
    IF_NONE_MATCH = "If-None-Match"

    # Custom Headers
    X_REQUESTED_WITH = "X-Requested-With"
    X_FORWARDED_FOR = "X-Forwarded-For"


class ResponseHeader(Enum):
    CONTENT_TYPE = "Content-Type"
    CONTENT_LENGTH = "Content-Length"
    CONTENT_ENCODING = "Content-Encoding"
    CACHE_CONTROL = "Cache-Control"
    ETAG = "ETag"
    EXPIRES = "Expires"
    LAST_MODIFIED = "Last-Modified"
    LOCATION = "Location"
    SET_COOKIE = "Set-Cookie"
    WWW_AUTHENTICATE = "WWW-Authenticate"
    ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    ACCESS_CONTROL_ALLOW_METHODS = "Access-Control-Allow-Methods"
    ACCESS_CONTROL_ALLOW_HEADERS = "Access-Control-Allow-Headers"
    SERVER = "Server"
    DATE = "Date"
    RETRY_AFTER = "Retry-After"


def isHeaderValid(header: str, header_type: HeaderType):

    if header_type == HeaderType.REQUEST_HEADER:
        request_headers = [h.name for h in RequestHeader]
        if header in request_headers:
            return True
    elif header_type == HeaderType.RESPONSE_HEADER:
        response_headers = [h.name for h in ResponseHeader]
        if header in response_headers:
            return True
        
    return False


def isHeaderSyntaxValid(header_type: HeaderType, regexp):
    pass


def validateToken(token: str) -> bool:
    tchar = "!#$%&'*+-.^_`|~0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    regex = rf"[^{tchar}]"
    res = re.search(regex, tchar)
    if res is None:
        return True 
    return False 


@dataclass
class Parameter():
    name: str 
    value: str = None


@dataclass
class MediaTypeMD():
    type: str
    subtype: str 
    weight: int = 1
    parameters: list[Parameter]


# check if the accept syntax is valid or not
def parseAccept(acceptVal: str) -> MediaTypeMD:
    vals = acceptVal.split(",")
    media_type_md: list[MediaTypeMD] = []

    for val in vals:
        tokens = val.split(";")
        media_type = tokens[0].split("/")
        type = media_type[0]
        subtype = media_type[1]
        params: list[Parameter] = []
        weight = 1
        if len(tokens) >= 2:
            for token in tokens[1::]:
                if "=" in token:
                    key, val = token.split("=")
                    if key == "q":
                        weight = 1 if float(val) > 1 else float(val)
                        continue
                    param = Parameter(name=key, value=val)
                    params.append(param)
                    continue
                param = Parameter(name=token)
                params.append(param)
        mtmd = MediaTypeMD(type, subtype, weight, params)
        media_type_md.append(mtmd)
    return media_type_md


@dataclass
class CharsetMD():
    charset: str 
    weight: int = 1

# Accept Charset parsing
def parseAcceptCharset(fieldVal: str):
    tokens = fieldVal.split(",")
    charset_md_lst: list[CharsetMD] = []
    for token in tokens:
        _p = token.split(";")
        charset, weight = _p if len(_p) == 2 else [_p[0], "q=1"]
        weight = float(weight.split("=")[1])
        charset_md = CharsetMD(charset, weight)
        charset_md_lst.append(charset)