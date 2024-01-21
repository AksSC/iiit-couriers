import os
from flask import redirect, render_template, request, session
from functools import wraps

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# It is required to set environment variables!
my_email = os.environ["MY_EMAIL"]
password_key = os.environ["MY_PASSWORD"]

gmail_server = "smtp-mail.outlook.com"
gmail_port = 587

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



def otp_mail(id, otp, toMail):
    my_server = smtplib.SMTP(gmail_server, gmail_port)
    my_server.ehlo()
    my_server.starttls()
    my_server.login(my_email, password_key)

    email_text = f"""Hi, your package number {id} is waiting for you at Nilgiri! OTP to collect your package is {otp}.\nKindly share this with the guard to collect your package and make sure to collect it as soon as possible!\n"""
    message = MIMEMultipart()
    message["From"] = my_email
    message["To"] = toMail
    message["Subject"] = "Your courier is here!"
    message.attach(MIMEText(email_text, "plain"))

    my_server.sendmail(my_email, toMail, message.as_string())

    my_server.quit()

def password_mail(id, password, toMail):
    my_server = smtplib.SMTP(gmail_server, gmail_port)
    my_server.ehlo()
    my_server.starttls()
    my_server.login(my_email, password_key)

    email_text = f"""Hello, you've been registered on courierIIIT and your credentials are:\nUsername/Id: {id}\nPassword: {password}\n"""
    message = MIMEMultipart()
    message["From"] = my_email
    message["To"] = toMail
    message["Subject"] = "Welcome to courierIIIT!"
    message.attach(MIMEText(email_text, "plain"))

    my_server.sendmail(my_email, toMail, message.as_string())

    my_server.quit()

def resend_mail(id, otp, toMail):
    my_server = smtplib.SMTP(gmail_server, gmail_port)
    my_server.ehlo()
    my_server.starttls()
    my_server.login(my_email, password_key)

    email_text = f"""Hello, you've requested a new OTP for your package number {id}. The new OTP is {otp}.\nKindly provide security with these details to collect as soon as possible!"""
    message = MIMEMultipart()
    message["From"] = my_email
    message["To"] = toMail
    message["Subject"] = "OTP for Courier!"
    message.attach(MIMEText(email_text, "plain"))

    my_server.sendmail(my_email, toMail, message.as_string())

    my_server.quit()

def recd_mail(id, toMail):
    my_server = smtplib.SMTP(gmail_server, gmail_port)
    my_server.ehlo()
    my_server.starttls()
    my_server.login(my_email, password_key)

    email_text = f"""Hello, your package number {id} has been collected!"""
    message = MIMEMultipart()
    message["From"] = my_email
    message["To"] = toMail
    message["Subject"] = "Courier Collected!"
    message.attach(MIMEText(email_text, "plain"))

    my_server.sendmail(my_email, toMail, message.as_string())

    my_server.quit()

def reformat_date(date):
    if date == "-":
        return "-"
    date_items = date.split("-")
    return date_items[2] + "/" + date_items[1] + "/" + date_items[0]

def reformat_time(time):
    if time == "-":
        return "-"
    time_items = time.split(":")
    return time_items[0] + ":" + time_items[1]

