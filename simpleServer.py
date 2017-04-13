 # -*- coding:utf-8 -*-
import thread
import os
import sys
import json
import time
import tornado.httpserver
import tornado.web
import tornado.ioloop
import thread
from tornado import websocket
import random
import uuid
import sys
import serial
import string
#import SendMail
#import identify
#import Students
reload(sys)
sys.setdefaultencoding('utf-8')
listenPort=80

class LogIndex(tornado.web.RequestHandler):
    def get(self):
        #loginState=self.get_secure_cookie("token")
        #cardNumber=self.get_secure_cookie("cardNumber")
        #username=self.get_secure_cookie("userName")
        #if(loginState=="logined" and cardNumber=="213142288"):
        f=open("20170321.txt","r")
        cont=f.read()
        cont=cont.replace("\n","<br>")
        self.write(cont)
        f.close()
        #else:
        #    self.write("No permission!")

if __name__ == '__main__':
    app = tornado.web.Application([
        ('/log', LogIndex)
    ],cookie_secret='abcdswweww2!!wsws2',
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "/home/pi/sniff"),
    )
    print "Running"
    app.listen(listenPort)
    tornado.ioloop.IOLoop.instance().start()

