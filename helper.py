import os
from flask import redirect, render_template, request, session
from functools import wraps

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

my_email = "courieriiit@outlook.com"
# Should I do this?
password_key = "LJ_23sux"

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