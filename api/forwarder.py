# Script to forward emails from your website to your email.
# Bypasses CORS error.

from flask import Flask, Response, request
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

print("SOMETHING")

sender = "fromemail@gmail.com (enable less secure app access in gmail)"
reciever = "recieveremail@gmail.com"
password = "REPLACE WITH YOUR APP PASSWORD (account.google.com/apppasswords)"

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


@app.route('/*', methods=['POST', 'GET'])
def forward():
    print("REQUEST RECIEVED")

    
    data = request.get_data()
    print(data)
    jsdata = json.loads(request.get_data().decode())

    subject = jsdata.get("subject")
    body = jsdata.get("body")
    reply = jsdata.get("reply")

    if not subject or not body or not reply:
        return Response("Not all parameters supplied.", 400)
    
    if send_email(subject, body, reply) == 200:
        return Response("Email sent successfully")
    
    return Response("Internal server error", 500)
    


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)