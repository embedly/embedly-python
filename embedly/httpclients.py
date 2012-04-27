"""
Httpclients
======

An http client has a request() method that accepts the following arguments:
    url: the URL being requested
    headers: a dictionary of headers to use with the request

request() returns a dictionary of response headers and the body of the response

Here are 2 HTTP clients, feel free to use your own
"""
import urllib2
import httplib2

class Httplib2Client(object):
    def __init__(self, timeout=30):
        self.timeout = timeout

    def request(self, url, headers=None):
        """
        Makes HTTP requests using httplib2
        """
        http = httplib2.Http(timeout=self.timeout)
        resp, content = http.request(url, headers=headers)

        return resp, content


class Urllib2Client(object):
    def __init__(self, timeout=30):
        self.timeout = timeout

    def request(self, url, headers=None):
        """
        Makes HTTP requests using urllib2
        """
        try:
            request = urllib2.Request(url, headers=(headers or {}))
            response = urllib2.urlopen(request, timeout=self.timeout)
            resp = response.headers.dict
            if "status" not in resp:
                resp["status"] = str(response.code)
            content = response.read()
        except urllib2.HTTPError, e:
            resp = {"status" : str(e.getcode())}
            content = e.read()

        return resp, content
