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
import logging

urls = (
  '/gvservice/convert/', 'convert',
  '/gvservice/dotimage/', 'dotimage',
) 

app = web.application(urls, globals())
# debug/trace flag
#simulate = 1
#logging.basicConfig(level=logging.DEBUG)

simulate = 0
logging.basicConfig(logfile='webpydot.log', level=logging.INFO)

def writefile(filename, contents):
    """
     write contents into a file
    """
    logging.debug("writefile: %s" % filename)
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
        logging.debug("Payload: %s" % payload)
        ts = time.time()
        filepath = storeFilename('convert', 'graphviz', '.dot', ts)
        pngfilepath = storeFilename('convert', 'graphviz', '.png', ts)
        if payload:
            writefile(filepath, payload)
            if not simulate:
                g=pydot.graph_from_dot_file(filepath)
                g.write_png(pngfilepath)
            #body of response contains the .png file
            #ret = loadfile(pngfilepath)
            #print "Produced a png of size %d bytes" % len(ret)
            
            #body of response contains the URL of .png resource
            ret = pngfilepath
            logging.info("png file generated at %s" % ret)
            return ret
        else:
            return "Error: Incorrect payload."
 
class dotimage:
    def GET(self):
        i = web.input()
        id = i.id
        if id:
            filename = id
            payload = loadfile(filename)
            web.header("Content-Type","image/png")
            return payload
        else:
            return 'File not found'

if __name__ == "__main__": 
    logging.info('Starting webpydot v%s' % __version__)
    app.run()

