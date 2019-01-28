import BaseHTTPServer
import sys
import urllib
import urllib2
from cgi import parse_header, parse_multipart
from urlparse import parse_qs

PORT = 8000

class proxyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        #Send Request to destination Host.
        request_headers = self.headers
        req = urllib2.Request(self.path)

        #Add All headers to request message
        for header in request_headers.headers:
            header_parts = header.split(':')
            if (len(header_parts) == 2):
                req.add_header(header_parts[0].strip(), header_parts[1].strip())

        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError as error:
            if error.getcode():
                resp = error
            else:
                print 'Proxy Error: Could not send GET to Server'

        self.send_response(resp.getcode())
        responseHeaders = resp.info()

        #Populate Headers in Response
        for header in responseHeaders:
            header_parts = header.split(':')
            if (len(header_parts) == 2):
                self.send_header(*header_parts)

        self.end_headers()

        #Write any body data
        self.wfile.write(resp.read())

        return

    def parse_POST(self):
        content_type, post_dict = parse_header(self.headers['content-type'])

        if content_type == 'multipart/form-data':
            post_vars = parse_multipart(self.rfile, post_dict)
        elif content_type == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            """
            NOTE: parse_qs will store each value as a list variable in the dictionary post_vars. It seems that when that
            happens, the data is corrupted after url encoding. So we are using the first value in the list if there is only
            one item. *A quick fix.
            """
            post_vars = dict( (k, v if len(v) > 1 else v[0] ) for k, v in parse_qs(self.rfile.read(length)).iteritems() )
        else:
            post_vars = {}

        return post_vars


    def do_POST(self):
        # Send Request to destination Host.
        request_headers = self.headers
        req = urllib2.Request(self.path)
        content_type_header = {}

        # Add All headers to request message
        for header in request_headers.headers:
            header_parts = header.split(':')
            if (len(header_parts) == 2):
                req.add_header(header_parts[0].strip(), header_parts[1].strip())

        # Add Any Form Data to the POST request
        data =  urllib.urlencode(self.parse_POST())

        try:
            resp = urllib2.urlopen(req, data=data)
        except urllib2.HTTPError as error:
            if error.getcode():
                resp = error
            else:
                print 'Proxy Error: Could not send GET to Server'
        except:
            print 'Unexpected error occured', sys.exc_info()[0]

        self.send_response(resp.getcode())
        responseHeaders = resp.info()

        # Populate Headers in Response
        for header in responseHeaders:
            header_parts = header.split(':')
            if (len(header_parts) == 2):
                self.send_header(*header_parts)

        self.end_headers()

        # Write any body data
        self.wfile.write(resp.read())

        return

try:
    proxyServer = BaseHTTPServer.HTTPServer(('', PORT), proxyRequestHandler)
    print 'Proxy Server listening on PORT:', PORT

    proxyServer.serve_forever()

except KeyboardInterrupt:
    proxyServer.server_close()
    print "Closing Server"
except ValueError:
    print 'Error converting data to integer'
except:
    print 'Unexpected error occured', sys.exc_info()[0]
    raise
