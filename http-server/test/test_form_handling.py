import unittest
from simple_server.form_handling import URLEncodedForm, MultipartForm, JSONDataHandling, OpSeqInvalidException, UnsupportedMediaTypeException


"""
1. test if method, path, protocol is properly collected using get_request_line()
2. test if host, content-type and content-length are properly extracted from string
3. test if exception is raised when validate_content_type is not called in sequence
4. test if the content_type is valid
5. test if the content_type is invalid
6. test the parsing of body data
7. test the submit functionality
"""


class URLEncodedFormTest(unittest.TestCase):
    
    def setUp(self):
     self.request_body1 = '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 27\r
\r
field1=value1&field2=value2'''
          
     self.request_body2 =  '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/json\r
Content-Length: 27\r
\r
field1=value1&field2=value2'''

     self.request_body3 = '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: ab\r
\r
field1=value1&field2=value2'''

    def test_get_request_line(self):
        form = URLEncodedForm(request_body=self.request_body1)
        form.get_request_line()
        self.assertEqual(form.method, 'POST')
        self.assertEqual(form.path, '/test')
        self.assertEqual(form.protocol, 'HTTP/1.1')

    def test_extract_header(self):
        form = URLEncodedForm(request_body=self.request_body1)
        form.extract_header()
        self.assertEqual(form.host, "example.com")
        self.assertEqual(form.content_type, "application/x-www-form-urlencoded")
        self.assertEqual(form.content_length, 27)
        form = URLEncodedForm(request_body=self.request_body3)
        form.extract_header()
        self.assertIsNone(form.request_body)

    def test_validate_content_type(self):
        f1 = URLEncodedForm(self.request_body1)
        f2 = URLEncodedForm(self.request_body2)
        
        with self.assertRaises(OpSeqInvalidException):
            f1.validate_content_type()
        
        f1.extract_header()
        f2.extract_header()
        self.assertTrue(f1.validate_content_type())
        self.assertFalse(f2.validate_content_type())

    def test_parse_data(self):
        success_d = {"field1": "value1", "field2": "value2"}
        form = URLEncodedForm(self.request_body1)

        with self.assertRaises(OpSeqInvalidException):
            form.parse_data()
        
        form.extract_header()
        form.validate_content_type()
        form.parse_data()
        self.assertEqual(form.form_data, success_d)

    def test_submit(self):
        success_d = {"field1": "value1", "field2": "value2"}
        form = URLEncodedForm(request_body=self.request_body1)
        form.submit()
        self.assertEqual(form.method, 'POST')
        self.assertEqual(form.path, '/test')
        self.assertEqual(form.protocol, 'HTTP/1.1')

        self.assertEqual(form.host, "example.com")
        self.assertEqual(form.content_type, "application/x-www-form-urlencoded")
        self.assertEqual(form.content_length, 27)

        self.assertEqual(form.form_data, success_d)
        form = URLEncodedForm(request_body=self.request_body2)
        with self.assertRaises(UnsupportedMediaTypeException):
            form.submit()


class MultipartformTest(unittest.TestCase):
        
        def setUp(self):
          self.request_body1 = """POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: multipart/form-data;boundary="delimiter12345"\r
\r
--delimiter12345\r
Content-Disposition: form-data; name="field1"\r
\r
value1\r
--delimiter12345\r
Content-Disposition: form-data; name="field2"; filename="example.txt"\r
\r
value2\r
--delimiter12345--\r
"""
          self.request_body2 = """POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: text/css;boundary="delimiter12345"\r
\r
--delimiter12345\r
Content-Disposition: form-data; name="field1"\r
\r
value1\r
--delimiter12345\r
Content-Disposition: form-data; name="field2"; filename="example.txt"\r
\r
value2\r
--delimiter12345--\r
"""

        def test_get_request_line(self):
                mf = MultipartForm(self.request_body1)
                mf.get_request_line()
                self.assertEqual(mf.method, "POST")
                self.assertEqual(mf.path, "/test")
                self.assertEqual(mf.protocol, "HTTP/1.1")

        def test_extract_header(self):
            mf = MultipartForm(self.request_body1)
            mf.extract_header()
            self.assertEqual(mf.boundary, "delimiter12345")
            self.assertEqual(mf.host, "example.com")
            self.assertEqual(mf.content_type, "multipart/form-data")            

        def test_validate_content_type(self):
             mf = MultipartForm(self.request_body1)
             with self.assertRaises(OpSeqInvalidException):
                  mf.validate_content_type()
             mf.extract_header()
             self.assertTrue(mf.validate_content_type())
             mf = MultipartForm(self.request_body2)
             mf.extract_header()
             self.assertFalse(mf.validate_content_type())

        def test_parse_data(self):
             mf = MultipartForm(self.request_body2)
             mf.extract_header()
             with self.assertRaises(UnsupportedMediaTypeException):
                  mf.parse_data()

             mf = MultipartForm(self.request_body1)
             mf.extract_header()
             mf.parse_data()
             form_data = [
                {
                    "name": "field1",
                    "value": "value1",
                    "attrs": {}
                },
                {
                     "name": "field2",
                     "value": "value2",
                     "attrs": {
                          "filename": "example.txt"
                     }
                }
             ]
             self.assertEqual(mf.form_data, form_data)

        def test_submit(self):
             mf = MultipartForm(self.request_body1)
             mf.submit()

             self.assertEqual(mf.method, "POST")
             self.assertEqual(mf.path, "/test")
             self.assertEqual(mf.protocol, "HTTP/1.1")

             self.assertEqual(mf.boundary, "delimiter12345")
             self.assertEqual(mf.host, "example.com")
             self.assertEqual(mf.content_type, "multipart/form-data")

             form_data = [
                {
                    "name": "field1",
                    "value": "value1",
                    "attrs": {}
                },
                {
                     "name": "field2",
                     "value": "value2",
                     "attrs": {
                          "filename": "example.txt"
                     }
                }
             ]
             self.assertEqual(mf.form_data, form_data)


class JSONDataHandlingTest(unittest.TestCase):
     
     def setUp(self):
          self.request_body1 = """POST /api/endpoint HTTP/1.1\r
Host: example.com\r
Content-Type: application/json\r
Content-Length: 49\r
\r
{\r
  "username": "jayesh",\r
  "password": "1234"\r
}\r
"""
          self.request_body2 = '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 27\r
\r
field1=value1&field2=value2'''

          self.json_handler1 = JSONDataHandling(self.request_body1)
          self.json_handler2 = JSONDataHandling(self.request_body2)

     def tearDown(self):
         self.json_handler1 = None
         self.json_handler2 = None 
     
     def test_get_request_line(self):
         self.json_handler1.get_request_line()
         self.assertEqual(self.json_handler1.method, "POST")
         self.assertEqual(self.json_handler1.path, "/api/endpoint")
         self.assertEqual(self.json_handler1.protocol, "HTTP/1.1")
     
     def test_extract_header(self):
         self.json_handler1.extract_header()
         self.assertEqual(self.json_handler1.host, "example.com")
         self.assertEqual(self.json_handler1.content_type, "application/json")
         self.assertEqual(self.json_handler1.content_length, 49)
     
     def test_validate_content_type(self):
          self.json_handler1.get_request_line()
         
          with self.assertRaises(OpSeqInvalidException):
             self.json_handler1.validate_content_type()
          self.json_handler1.extract_header()
          self.assertTrue(self.json_handler1.validate_content_type())

          self.json_handler2.extract_header()
          self.assertFalse(self.json_handler2.validate_content_type())
         
     def test_parse_data(self):
          with self.assertRaises(OpSeqInvalidException):
             self.json_handler1.parse_data()
          self.json_handler1.extract_header()
          self.json_handler1.parse_data()
          json_obj = {"username": "jayesh", "password": "1234"}
          self.assertDictEqual(self.json_handler1.json_data, json_obj)

          self.json_handler2.extract_header()
          with self.assertRaises(UnsupportedMediaTypeException):
              self.json_handler2.parse_data()
     
     def test_submit(self):
          self.json_handler1.submit()
          json_obj = {"username": "jayesh", "password": "1234"}
          self.assertEqual(self.json_handler1.method, "POST")
          self.assertEqual(self.json_handler1.path, "/api/endpoint")
          self.assertEqual(self.json_handler1.protocol, "HTTP/1.1")
          self.assertEqual(self.json_handler1.host, "example.com")
          self.assertEqual(self.json_handler1.content_type, "application/json")
          self.assertEqual(self.json_handler1.content_length, 49)
          self.assertTrue(self.json_handler1.validate_content_type())
          self.assertDictEqual(self.json_handler1.json_data, json_obj)