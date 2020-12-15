# - * - coding: utf - 8 -*-
#
# 作者：田丰
# 邮箱：fonttian@163.com
# 撰写时间：2017年4月22日
# Python版本：3.6.1
# CSDN：http://blog.csdn.net/fontthrone
#
import smtplib
import email.mime.multipart import MIMEMultipart
import email.mime.text import MIMEText
 
msg = MIMEMultipart()
msgFrom = '748862180@qq.com' #从该邮箱发送
sqm='mjeigilwlzvxbcfg' # 在登录smtp时需要login中的密码应当使用授权码而非账户密码
msgTo = '1640464937@qq.com' #发送到该邮箱
smtpSever='smtp.qq.com' # 163邮箱的smtp Sever地址
# smtpPort = '25' #开放的端口

 
msg['from'] = msgFrom
msg['to'] = msgTo
msg['subject'] = 'Python自动邮件-'+dataNumber
content = '''
你好:
  这是一封python3发送的邮件
'''
txt = MIMEText(content)
msg.attach(txt)
xlsxpart = MIMEApplication(open('F:/jenkins_workspace/workspace/youtime/report/example_requests.csv', 'rb').read())
xlsxpart.add_header('Content-Disposition', 'attachment', filename='example_requests.csv')
msg.attach(xlsxpart)
smtp = smtplib.SMTP()
'''
smtplib的connect（连接到邮件服务器）、login（登陆验证）、sendmail（发送邮件）
'''
smtp.connect(smtpSever)
smtp.login(msgFrom, sqm)
smtp.sendmail(msgFrom, msgTo, str(msg))
smtp.quit()