#!/usr/bin/env python
"""
Test web service

"""
import httplib

hostname = "localhost"
port = 8080

f = open('sample.dot')
body=f.read()
f.close()

conn = httplib.HTTPConnection(hostname, port)
conn.request("POST", "/gvservice/convert/", body)
response = conn.getresponse()
print response.status, response.reason
res = response.read()
print "Received %d bytes" % len(res)
conn.close()
