'''
Created on Jul 23, 2014

@author: zking
'''

import smtplib
from email.mime.text import MIMEText


class Email(object):
    
    def __init__(self, host, user, password, sender, use_tls=False):
        self.host = host
        self.user = user
        self.password = password
        self.sender = sender
        self.use_tls = use_tls
    
    
    def send(self, receiver, subject, text):

        msg = MIMEText(text, 'html')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = receiver
        
        server = smtplib.SMTP(self.host)
        
        if self.use_tls:
            server.ehlo()
            server.starttls()
            
        server.login(self.user,self.password)
        server.sendmail(self.sender, receiver, msg.as_string())
