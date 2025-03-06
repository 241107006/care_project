
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
import os

msg = MIMEMultipart()
msg['From'] = 'zabotapluss@gmail.com'
msg['To'] = '200103395@stu.sdu.edu.kz'
msg['Subject'] = 'test'
msg.attach(MIMEText('body', 'plain'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('zabotapluss@gmail.com', 'zabotazabotazabota')

    server.sendmail('zabotapluss@gmail.com', '200103395@stu.sdu.edu.kz', msg.as_string())
    server.close()
    print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email. Error: {e}")