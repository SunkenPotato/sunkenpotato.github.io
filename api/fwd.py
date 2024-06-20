

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.server import BaseHTTPRequestHandler
import os
import json
import smtplib

sender = os.environ.get("SMTP_SENDER")
reciever = os.environ.get("SMTP_RECIEVER")
password = os.environ.get("SMTP_PASSWORD")
server_addr = os.environ.get("SMTP_SERVER")


def send_email(subject: str, body: str, reply: str):

    body = "Reply at: " + reply + "\n" + body

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = reciever
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(server_addr, 587)
    
        server.starttls()
        server.login(sender, password)
    
        text = message.as_string()
    
        server.sendmail(sender, reciever, text)

        return True
    except Exception as e:
        print(f"An unexpected error ocurred: {e}")
        return False
    finally: 
        server.quit()

    

class handler(BaseHTTPRequestHandler):

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(handler, self).end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        print(f"Request recieved from {self.client_address[0]}")

        # client_auth = self.headers.get("x-api-auth")
        # if not client_auth and not client_auth == key:
        #    self.send_response_only(403)
        #    self.end_headers()
        #    return
        
        try: 
            content_length = int(self.headers.get('Content-Length'))
        except TypeError: 
            self.send_response_only(400, "Content-Length missing")
            return
        
        post_body = self.rfile.read(content_length)
        post_body: dict = json.loads(post_body)

        about = post_body.get('about')
        body = post_body.get('body')
        reply = post_body.get('from')

        print(post_body)

        if not about or not body or not reply:
            self.send_response_only(400, 'Check if all fields have been submitted correctly')
            return
        
        if send_email(about, body, reply):
            self.send_response_only(200)
            return
        
        self.send_response_only(500, "Internal server error")