#!/usr/bin/python
import pycurl
from io import BytesIO
from StringIO import StringIO

message = '''\
Content-Type: text/html; charset="us-ascii"
Content-Transfer-Encoding: quoted-printable
Mime-version: 1.0
To: dmz.oneill@gmail.com
Subject: AYC - Heat status change (state)

changed state

'''

class Email:
    
    def __init__(self):
        pass

    def file_get_contents(self, filename):
        with open(filename) as f:
            return f.read()

    def send_email(self, state):
        global message
        copy = message.replace("state", state)
        io = BytesIO(copy)
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'smtps://smtp.gmail.com:465')
        c.setopt(c.MAIL_FROM, "suicidalbeanbag@gmail.com")
        c.setopt(c.MAIL_RCPT, ["dmz.oneill@gmail.com"])
        c.setopt(c.USERPWD, "suicidalbeanbag@gmail.com" + ":" + self.file_get_contents("/var/lib/motion/.google-app-password"))
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.READDATA, io)
        c.setopt(c.UPLOAD, True)
        c.setopt(c.VERBOSE, True)
        c.perform()
        c.close()
        body = buffer.getvalue()
        #print(body)
