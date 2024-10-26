
# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mail:

    smtp_server = None
    smtp_port = None
    smtp_username = None
    smtp_password = None
    from_address = None


    def __init__(self, from_address, smtp_server, smtp_port, smtp_username, smtp_password):

        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

        self.from_address = from_address
       
    
    def send_mail(self, to_address, subject, body):
        
        try:
            
            message = MIMEMultipart()
            message['From'] = self.from_address
            message['To'] = ", ".join(to_address)

            message.attach(MIMEText(body, 'html'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)

                message['Subject'] = subject

                for address in to_address:
                    print('Enviando correo a ' + address)
                    server.sendmail(self.from_address, address, message.as_string())

            return True

        except Exception as e: 
            return e
    