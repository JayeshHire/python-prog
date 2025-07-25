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

