# httpProxyServer
Simple Proxy server for HTTP requests 

Written in Python 2.7 on Ubuntu 16.xx

The server was implemented as a test and only supports GET and POST commands. 

Example Usage:

$curl -x http://localhost:8000/ http://httpbin.org/get
{
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "identity", 
    "Connection": "close", 
    "Host": "httpbin.org", 
    "Proxy-Connection": "Keep-Alive", 
    "User-Agent": "curl/7.47.0"
  }, 
  "origin": "99.237.73.189", 
  "url": "http://httpbin.org/get"
}

$curl -d asdf=blah -x http://localhost:8000/ http://httpbin.org/post
{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "asdf": "blah"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "identity", 
    "Connection": "close", 
    "Content-Length": "9", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "httpbin.org", 
    "Proxy-Connection": "Keep-Alive", 
    "User-Agent": "curl/7.47.0"
  }, 
  "json": null, 
  "origin": "99.237.73.189", 
  "url": "http://httpbin.org/post"
}


