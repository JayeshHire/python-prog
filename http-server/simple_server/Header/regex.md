## Regular expressions for each of the header fields

token = 1*tchar
tchar = "!" / "#" / "$" / "%" / "&" / "'" / "*" / "+" / "-" / "." /
     "^" / "_" / "`" / "|" / "~" / DIGIT / ALPHA


1. Accept ABNF
Accept = #( media-range [ accept-params ] )
media-range    = ( "*/*" / ( type "/" "*" ) / ( type "/" subtype ) )
type           = token
subtype        = token
accept-params  = weight *accept-ext
weight         = OWS ";" OWS "q=" qvalue
qvalue         = ( "0" [ "." 0*3DIGIT ] )
               / ( "1" [ "." 0*3("0") ] )
accept-ext     = OWS ";" OWS token [ "=" ( token / quoted-string ) ]

    -- Example:
    1. accept-ext: Optional parameter given by the servers.
        
        `Accept: text/html;q=0.9;theme=dark;lang="en-GB"`


2. Accept-Charset
Accept-Charset = 1#( ( charset / "*" ) [ weight ] )

charset        = token

weight         = OWS ";" OWS "q=" qvalue

qvalue         = ( "0" [ "." 0*3DIGIT ] )
               / ( "1" [ "." 0*3("0") ] )

    --Example
    1. Accept-Charset: utf-8;q=1.0, iso-8859-1;q=0.5


3. Accept-Encoding = #( codings [ weight ] )

codings         = content-coding / "identity" / "*"

content-coding  = token

weight          = OWS ";" OWS "q=" qvalue

    --Example
    1. Accept-Encoding: gzip, deflate
    2. Accept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1


4. Accept-Language
The Accept-Language header is used by the client to tell the server which natural language it prefers. This helps in language negotiations, so that the server can respond in that language.

* ABNF
Accept-Language = #( language-range [ weight ] )

language-range  = (1*8ALPHA *("-" 1*8alphanum)) / "*"

weight          = OWS ";q=" qvalue

qvalue          = ( "0" [ "." 0*3DIGIT ] )
                / ( "1" [ "." 0*3("0") ] )

OWS             = *( SP / HTAB )  ; optional whitespace

Accept-Language: en-US,en;q=0.9,hi;q=0.8,de;q=0.7


5. Authorization
It is used for authenticating the client to server by providing credentials

It allows client to prove it's identity using following schemes:
    1. Basic
    2. Bearer
    3. Digest, HOBA, Mutual, AWS4-HMAC-SHA256

Authorization = credentials

credentials   = auth-scheme [ 1*SP ( token68 / auth-param *( OWS "," OWS auth-param ) ) ]

auth-scheme   = token
token68       = 1*( ALPHA / DIGIT / "-" / "." / "_" / "~" / "+" / "/" ) *"="
auth-param    = token "=" ( token / quoted-string )

    Schemes for authorization:
    1. Basic:
    Authorization: Basic jdheAChbKJ  ; here the "username:password" is encrypted using base64

    2. 
