#!/usr/bin/env python
import os, sys, os.path
from daemon import Daemon
from webpydot import app
DEBUG=1

"""
class Daemon:
    def start(self):
        #... PID CHECKS....

        # Start the daemon
        self.daemonize()
        self.run()
"""
#My code
class WebpydotDaemon(Daemon):
    
    #def __init__(self, pidfile):
    #    super(self,pidfile)
        
    def run(self):
        app.run()

if __name__ == "__main__":
    if DEBUG:
        app.run()
    else:
        service = WebpydotDaemon(os.path.join('/tmp','webpydot.pid'))
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                sys.argv[1] = '8080'
                service.start()        
            elif 'stop' == sys.argv[1]:
                service.stop()
            elif 'restart' == sys.argv[1]:
                service.restart()
            else:
                print "Unknown command"
                sys.exit(2)
            sys.exit(0)
        else:
            print "usage: %s start|stop|restart" % sys.argv[0]
            sys.exit(2)
