#!/usr/bin/python

import pycurl
from io import BytesIO
from StringIO import StringIO

recipient = "dmz.oneill@gmail.com"
fromemail = "suicidalbeanbag@gmail.com"
fromname = "Rick James"

message = '''\
From: "%s" <%s>
To: %s
Subject: AYC - Heat status change

SMTP example via PycURL

''' % (fromemail, fromname, recipient)

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

def send_email():
    io = BytesIO(message)
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'smtps://smtp.gmail.com:465')
    c.setopt(c.MAIL_FROM, fromemail)
    c.setopt(c.MAIL_RCPT, [recipient])
    c.setopt(c.USERPWD, fromemail + ":" + file_get_contents("/var/lib/motion/.google-app-password"))
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.READDATA, io)
    c.setopt(c.UPLOAD, True)
    c.setopt(c.VERBOSE, True)
    c.perform()
    c.close()

    body = buffer.getvalue()
    # Body is a string in some encoding.
    # In Python 2, we can print it without knowing what the encoding is.
    print(body)

send_email()