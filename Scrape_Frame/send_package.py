# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders

userlist = [
{'name': 'Onns', 'email': 'onns@onns.xyz'}, 
{'name': 'XX', 'email': '756970920@qq.com'},
]

for user in userlist:
	content = ''
	mail_host="smtp.mxhichina.com"  
	mail_user="notification@onns.xyz"   
	mail_pass="Abcd1234"   
	sender = 'notification@onns.xyz'
	receivers = [user['email']]
	# message = MIMEText(content, 'html', 'utf-8')
	message = MIMEMultipart()
	message['From'] = Header("Onns", 'utf-8')
	message['To'] =  Header(user['name'], 'utf-8')
	subject = 'data'
	message['Subject'] = Header(subject, 'utf-8')
	message.attach(MIMEText('', 'plain', 'utf-8'))
	att = MIMEText(open('20161006-1.tar.gz', 'rb').read(), 'base64', 'utf-8')
	att["Content-Type"] = 'application/octet-stream'
	att["Content-Disposition"] = 'attachment; filename="20161006-1.tar.gz"'
	message.attach(att)
	try:
	    smtpObj = smtplib.SMTP() 
	    smtpObj.connect(mail_host, 25)    
	    smtpObj.set_debuglevel(1)
	    smtpObj.login(mail_user,mail_pass)
	    smtpObj.sendmail(sender, receivers, message.as_string())
	    smtpObj.quit()
	    print ('邮件发送成功')
	except smtplib.SMTPException:
	    print ('无法发送邮件')
