from flask import Flask, Response, request
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

print("App launched")

sender = os.environ.get("SMTP_SENDER")
reciever = os.environ.get("SMTP_RECIEVER")
password = os.environ.get("SMTP_PASSWORD")

def send_email(subject: str, body: str, reply: str):

    body = "Reply at: " + reply + "\n" + body

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = reciever
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)

        text = message.as_string()

        server.sendmail(sender, reciever, text)

        return 200
    except Exception as e:
        print(f"An unexpected error ocurred: {e}")
        return 500

    finally: server.quit()


@app.route('/api/forward_email', methods=['POST'])
def forward():
    data = request.get_data()
    print(data)
    jsdata = json.loads(request.get_data().decode())

    subject = jsdata.get("about")
    body = jsdata.get("body")
    reply = jsdata.get("from")

    if not subject or not body or not reply:
        return Response("Not all parameters supplied.", 400)
    
    if send_email(subject, body, reply) == 200:
        return Response("Email sent successfully")
    
    return Response("Internal server error", 500)
    