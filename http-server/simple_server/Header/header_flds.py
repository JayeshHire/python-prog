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
    request_headers = [h.name for h in RequestHeader]
    response_headers = [h.name for h in ResponseHeader]

    if header_type == HeaderType.REQUEST_HEADER:
        if header in request_headers:
            return True
    elif header_type == HeaderType.RESPONSE_HEADER:
        if header in response_headers:
            return True
        
    return False