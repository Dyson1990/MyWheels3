# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 16:08:39 2022

@author: Weave
"""
import sys
from pathlib import Path

import smtplib

from email.message import EmailMessage
from email.headerregistry import Address

class Email:
    
    def __init__(self, my_email):
        self.msg = EmailMessage()
        self.msg['From'] = my_email
        self.my_email = my_email
    
    def write(self, subject, content, *addr_list):
        self.msg['Subject'] = subject
        self.msg.set_content(content)
        
        obj_list = []
        for addr0 in addr_list:
            obj_list.append(addr0)
            
        self.msg['To'] = tuple(obj_list)
    
    def send(self, host='localhost'):
        smtp = smtplib.SMTP(host)
        smtp.send_message(self.msg)
        smtp.quit()
        
class Email163(Email):
    
    def __init__(self, my_email):
        super(Email163,self).__init__(my_email)
        
    def send(self, pwd="GOELDMAMTDWBEPLG"):
        smtp = smtplib.SMTP_SSL("smtp.163.com", 465) # GOELDMAMTDWBEPLG
        smtp.login(self.my_email, pwd)
        smtp.send_message(self.msg)
        smtp.quit()
        

if __name__ == "__main__":
    e = Email163("Dyson1990@163.com")
    e.write("test", "test", "liuyingbo@trade-ai.com")
    e.send()