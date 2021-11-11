#!/usr/bin/python3.8
import ssl
import smtplib

class Mailer(object):
    def  __init__(self, *args, **kwargs):
        self.sender = 'example@example.com'
        self.rec = 'example@example.com'
        self.port = 465
        self.password = 'password'
        self.host = 'smtp host'
        self.context = ssl.create_default_context()


    def sendMessage(self, subject, from_sender, message):
        with smtplib.SMTP_SSL(self.host, self.port, self.context) as server:
            server.ehlo()
            server.login(self.sender, self.password)
            message =f"""From: {from_sender}\nSubject: {subject}\n{message}"""
            server.sendmail(self.sender, self.rec, message)
            server.quit()
