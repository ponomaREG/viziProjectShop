import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template

server = 'smtp.yandex.ru'
user = 'hpisda@yandex.ru'
pswd = 'why are you so curious'
sender = 'support@booker.ru'
msg = 'TEST'


class EmailSender:



    @staticmethod
    def sendEmailTo(recipients,orderDetails):
        msg = MIMEMultipart('alternative')
        msg['From'] = user
        msg['To'] = recipients[0]
        msg['Subject'] = 'Order №{} details'.format(orderDetails['id'])
        html = render_template('order-email.html',order = orderDetails)
        msg.attach(MIMEText(html,'html'))

        session = smtplib.SMTP_SSL(server)
        
        session.login(user=user,password=pswd)
        session.sendmail(user,recipients,msg.as_string())
        session.close()

    