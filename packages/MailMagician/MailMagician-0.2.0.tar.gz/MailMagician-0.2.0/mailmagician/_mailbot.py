import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Mailbot():
    def __init__(self,email_account:str, password:str, smtp_server:str ='smtp.126.com'):
        self.gmail_user = email_account
        self.gmail_password = password
        self.smtp_server = smtp_server

    def send(self,sentTo,subject,msgBody):
        gmail_user = self.gmail_user
        sent_from = self.gmail_user
        gmail_password = self.gmail_password
        email_text = msgBody

        msg = MIMEText(email_text,_charset= 'utf-8')
        msg["Subject"] = Header(subject, charset = 'utf-8')
        msg["From"] = gmail_user
        msg["To"] = sentTo

        try:
            server = smtplib.SMTP_SSL(self.smtp_server)
            server.ehlo()
            server.login(gmail_user, gmail_password)

            server.sendmail(sent_from,sentTo,msg.as_string())
            server.close()

            print('Email sent!')
        except Exception as e:
            print('Something went wrong...')
            raise e