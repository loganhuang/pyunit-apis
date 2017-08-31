#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from config.config import BaselineConfig
from common.const.const import PATH


class BaseLineEmail:
    def __init__(self, report_file):
        self.report = report_file
        self.config = BaselineConfig(PATH.CONFIG_INI_FILE)

    def send_email(self):
        f = open(self.report, 'rb')
        mail_body = f.read()
        f.close()

        # smtp server
        smtpserver = self.config.get_email_smtp()
        # user & password
        user = self.config.get_email_user()
        password = self.config.get_email_pwd()

        # receivers
        #receiver = ['572419627@qq.com', 'xulongqiu163@163.com']
        receiver = self.config.get_email_receiver().split(' ')
        # subject
        subject = '自动定时发送测试报告' + time.strftime('%Y%m%d%H%M%S')

        msg = MIMEMultipart('mixed')

        #    text = "Dear all!\nThe attachment is new testreport.\nPlease check it."
        #    msg_plain = MIMEText(text,'plain', 'utf-8')
        #    msg.attach(msg_plain)

        msg_html1 = MIMEText(mail_body, 'html', 'utf-8')
        msg.attach(msg_html1)

        msg_html = MIMEText(mail_body, 'html', 'utf-8')
        msg_html["Content-Disposition"] = 'attachment; filename="TestReport.html"'
        msg.attach(msg_html)

        msg['From'] = user
        msg['To'] = ";".join(receiver)
        msg['Subject'] = Header(subject, 'utf-8')

        # 连接发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, 25)
        smtp.login(user, password)
        smtp.sendmail(user, receiver, msg.as_string())
        smtp.quit()


if __name__ == '__main__':
    pass

