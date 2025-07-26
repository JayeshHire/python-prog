from unittest import TestCase
from header_flds import *


class ParseHeaderTest(TestCase):

    def test_parse_accept(self):
        accept = "text/html;q=0.9;theme=dark;lang=\"en-GB\""
        exp_res = [
            MediaTypeMD(type="text", 
                        subtype="html", 
                        weight=0.9, 
                        parameters= [
                            Parameter(name="theme", 
                                      value="dark"),
                            Parameter(name="lang",
                                      value="en-GB")
                        ]
                        ),
        ]
        act_res = parseAccept(accept)
        self.assertListEqual(exp_res, act_res, f"Actual response: {act_res}")

        accept="text/html, application/json;q=0.9, image/avif, */*"
        exp_res = [
            MediaTypeMD(
                type="text",
                subtype="html",
                weight=1
            ),
            MediaTypeMD(
                type="application",
                subtype="json",
                weight=0.9
            ),
            MediaTypeMD(
                type="image",
                subtype="avif",
                weight=1
            ),
            MediaTypeMD(
                type="*",
                subtype="*"
            )
        ]
        act_res = parseAccept(accept)
        self.assertListEqual(exp_res, act_res, f"Actual response: {act_res}")
    
    def test_parse_accept_charset(self):
        accept_charset = "utf-8;q=1.0, iso-8859-1;q=0.5, my-charset"
        exp_res = [
            CharsetMD(
                charset="utf-8",
                weight=1.0
            ),
            CharsetMD(
                charset="iso-8859-1",
                weight=0.5
            ),
            CharsetMD(
                charset="my-charset"
            )
        ]
        act_res = parseAcceptCharset(accept_charset)
        self.assertListEqual(exp_res, act_res, f"Actual response: {act_res}")
    
    def test_parse_accept_encoding(self):
        accept_encoding = "gzip, deflate"
        exp_res = [
            EncodingMD(
                name="gzip",
            ),
            EncodingMD(
                name="deflate"
            )
        ]
        act_res = parseAcceptEncoding(accept_encoding)

        accept_encoding = "br;q=1.0, gzip;q=0.8, *;q=0.1"
        exp_res = [
            EncodingMD(
                name="br",
                weight=1.0
            ),
            EncodingMD(
                name="gzip",
                weight=0.8
            ),
            EncodingMD(
                name="*",
                weight=0.1
            )
        ]
        act_res = parseAcceptEncoding(accept_encoding)
        self.assertListEqual(exp_res, act_res)

    def test_parse_accept_language(self):
        accept_language = "en-US,en;q=0.9,hi;q=0.8,de;q=0.7"
        exp_res = [
            Language(
                name="en-US"
            ),
            Language(
                name="en",
                weight=0.9
            ),
            Language(
                name="hi",
                weight=0.8
            ),
            Language(
                name="de",
                weight=0.7
            )
        ]
        act_res = parseAcceptLanguage(accept_language) 
        self.assertListEqual(exp_res, act_res)