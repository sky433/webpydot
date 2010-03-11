#!/usr/bin/env python

"""

 Simple service for graphviz dot file rendering.
 Uses webpy framework.
 
 To enable verbose mode, modify 'debug' flag.

"""

import time
import web
#import basicauth
from __init__ import __version__
#import settings
import pydot

urls = (
  '/gvservice/convert/', 'convert',
  #'/(.*)', 'index'
) 

app = web.application(urls, globals())
# debug/trace flag
debug = 0

def writefile(filename, contents):
    """
     write contents into a file
    """
    print filename
    file = open(filename, "w")
    file.write(contents)
    file.close()

def loadfile(filename):
    """
     Load file into a string
    """
    file = open(filename, "rb")
    ret = file.read()
    file.close()
    return ret

    

def storeFilename(dir, basename, ext, timestamp = 0):
    ip = web.ctx.environ['REMOTE_ADDR']
    if not timestamp:
        timestamp = time.time()
    filename = dir + '/'+ip+'-'+basename+'-'+str(int(timestamp)) + ext
    return filename

def storeFilenameLeaf(basename, ext, timestamp = 0):
    ip = web.ctx.environ['REMOTE_ADDR']
    if not timestamp:
        timestamp = time.time()
    filename = ip+'-'+basename+'-'+str(int(timestamp)) + ext
    return filename

class convert:
    def POST(self):
        """ Processes POST request, expecting .dot payload
         @return .png image represeting .dot
        """
        payload = web.data()
        if debug:
            print payload
        ts = time.time()
        filepath = storeFilename('convert', 'graphviz', '.dot', ts)
        pngfilepath = storeFilename('convert', 'graphviz', '.png', ts)
        if payload:
            writefile(filepath, payload)
            g=pydot.graph_from_dot_file(filepath)
            g.write_png(pngfilepath)
            ret = loadfile(pngfilepath)
            print "Produced a png of size %d bytes" % len(ret)
            return ret
        else:
            return "Error: Incorrect payload."
 

if __name__ == "__main__": 
    print 'Starting webpydot v'+__version__
    app.run()

