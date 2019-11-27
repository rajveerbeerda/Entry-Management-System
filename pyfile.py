# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:00:24 2019

@author: manmeet sethi
"""
import datetime
import pandas as pd
import re
class Visitor:
    def __init__(self, name, email, phone, host, address, checkin, checkout):
        self.name = name
        self.email = email
        self.phone=phone
        self.in_time=datetime.datetime.now()
        self.status=1
        self.host=host
        self.address=address
        self.checkin = checkin
        self.checkout = checkout

import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client 
MY_ADDRESS = 'rb5096@bennett.edu.in'
PASSWORD = 'BhebhaRAM@16'


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def host_mail(v, Email, phone):
    phone = '+'+str(phone)
    message_template = read_template('host.txt')

    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    message = message_template.substitute(PERSON_NAME=v.host, NAME=v.name, EMAIL=v.email, PHONE=str(v.phone))

    msg['From']=MY_ADDRESS
    msg['To']=Email
    msg['Subject']="Your Visitor is here "

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)
    del msg

    s.quit()

    account_sid = 'ACb1be356953a8858fc246e7a9dfebb367'
    auth_token = '2f8c222d8f4286b9d7b62dda5c9e758b'
    client = Client(account_sid, auth_token)
    message_send = client.messages.create(
                                  from_='+12055094353',
                                  body = message,
                                  to = phone
                              )

def sendTexts(visitorName, visitorEmail, visitorPhone, hostName, hostAddress, checkin):
    flag = 1

    key = str(hostName+str(hostAddress)).lower()

    host_df = pd.read_csv('host.csv', names=('Name', 'Phone', 'Email', 'Add'))
    key2=[]
    for index, row in host_df.iterrows():
        key2.append(str(row["Name"]+str(row["Add"])).lower())
    if key in key2:
        v=Visitor(visitorName, visitorEmail, visitorPhone, hostName, hostAddress, checkin, 'na')
    else:
        flag = 0
        return flag


    dict = {'name': v.name, 'email': v.email, 'phone': v.phone, 'host': v.host, 'address': v.address, 'status':v.status, 'checkin':v.checkin, 'checkout':'NA'}
    df = pd.DataFrame(dict, index=[1])
    df.to_csv(r'visitor.csv',mode='a', index=False, header=None)

    email=host_df.Email.values[host_df['Name'] == v.host]
    re.findall('\S+@\S+', email[0])

    Phone=host_df.Phone.values[host_df['Name'] == v.host]

    try:
        host_mail(v, email[0], str(Phone))
    except Exception as e:
        print(e)
        flag = 0

    return flag



def checkoutMail(v, Email, phone):
    if len(str(phone))<=10:
        phone = '+91'+str(phone)
    else:
        phone = str(phone)
    message_template = read_template('visitor.txt')

    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    message = message_template.substitute(VISITOR_NAME=v.name, EMAIL=v.email, PHONE=str(v.phone), HOST=v.host, ADDRESS=v.address, INTIME=v.checkin, OUTTIME=v.checkout)

    msg['From']=MY_ADDRESS
    msg['To']=Email
    msg['Subject']="Thank you for visiting Innovaccer."

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)
    del msg

    s.quit()

    account_sid = 'ACb1be356953a8858fc246e7a9dfebb367'
    auth_token = '2f8c222d8f4286b9d7b62dda5c9e758b'
    client = Client(account_sid, auth_token)
    message_send = client.messages.create(
                                  from_='+12055094353',
                                  body = message,
                                  to = phone
                              )

def checkoutTexts(visitorName, visitorEmail, visitorPhone, hostName, hostAddress, checkin, checkout):
    flag = 1
    try:
        v=Visitor(visitorName, visitorEmail, visitorPhone, hostName, hostAddress, checkin, checkout)
        checkoutMail(v, v.email, v.phone)
    except Exception as e:
        print(e)
        flag = 0

    return flag


