import unittest
from simple_server.form_handling import URLEncodedForm, OpSeqInvalidException, UnsupportedMediaTypeException
# from simple_server.form_handling import 


class URLEncodedFormTest(unittest.TestCase):

    def test_get_request_line(self):
        request_body = '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 27\r
\r
field1=value1&field2=value2'''
        form = URLEncodedForm(request_body=request_body)
        form.get_request_line()
        self.assertEqual(form.method, 'POST')
        self.assertEqual(form.path, '/test')
        self.assertEqual(form.protocol, 'HTTP/1.1')

    def test_extract_header(self):
        request_body = '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 27\r
\r
field1=value1&field2=value2'''
        form = URLEncodedForm(request_body=request_body)
        form.extract_header()
        self.assertEqual(form.host, "example.com")
        self.assertEqual(form.content_type, "application/x-www-form-urlencoded")
        self.assertEqual(form.content_length, 27)

        # check if the exception handling works properly
        request_body = '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: ab\r
\r
field1=value1&field2=value2'''
        form = URLEncodedForm(request_body=request_body)
        form.extract_header()
        self.assertIsNone(form.request_body)

    def test_validate_content_type(self):
        request_body1 = '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 27\r
\r
field1=value1&field2=value2'''

        request_body2 = '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/json\r
Content-Length: 27\r
\r
field1=value1&field2=value2'''

        f1 = URLEncodedForm(request_body1)
        f2 = URLEncodedForm(request_body2)
        
        with self.assertRaises(OpSeqInvalidException):
            f1.validate_content_type()
        
        f1.extract_header()
        f2.extract_header()
        self.assertTrue(f1.validate_content_type())
        self.assertFalse(f2.validate_content_type())

    def test_get_form_data(self):
        request_body = '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 27\r
\r
field1=value1&field2=value2'''

        success_d = {"field1": "value1", "field2": "value2"}
        form = URLEncodedForm(request_body)

        with self.assertRaises(OpSeqInvalidException):
            form.get_form_data()
        
        form.extract_header()
        form.validate_content_type()
        form.get_form_data()

        self.assertEqual(form.form_data, success_d)

    def test_submit(self):
        success_d = {"field1": "value1", "field2": "value2"}
        request_body = '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 27\r
\r
field1=value1&field2=value2'''
        form = URLEncodedForm(request_body=request_body)
        form.submit()
        self.assertEqual(form.method, 'POST')
        self.assertEqual(form.path, '/test')
        self.assertEqual(form.protocol, 'HTTP/1.1')

        self.assertEqual(form.host, "example.com")
        self.assertEqual(form.content_type, "application/x-www-form-urlencoded")
        self.assertEqual(form.content_length, 27)

        self.assertEqual(form.form_data, success_d)
        
        request_body = '''POST /test HTTP/1.1\r
Host: example.com\r
Content-Type: application/json\r
Content-Length: 27\r
\r
field1=value1&field2=value2'''
        form = URLEncodedForm(request_body=request_body)
        with self.assertRaises(UnsupportedMediaTypeException):
            form.submit()
