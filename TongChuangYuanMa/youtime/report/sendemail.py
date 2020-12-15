#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time

class Mailer(object):

  def __init__(self,maillist,mailtitle,mailcontent):
    self.mail_list = maillist
    self.mail_title = mailtitle
    self.mail_content = mailcontent
    ##### email服务器配置 #####
    self.mail_host = "smtp.qq.com"
    self.mail_user = "748862180@qq.com"
    self.mail_pass = "mjeigilwlzvxbcfg"
    self.mail_postfix = "qq.com"
 
  def sendMail(self):
    now = int(time.time())  #显示为时间戳
    timeArray = time.localtime(now)
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    me = self.mail_user + "<" + self.mail_user + "@" + self.mail_postfix + ">"
    msg = MIMEMultipart()
    msg['Subject'] = currentTime+'youtime测试报告'
    msg['From'] = me
    msg['To'] = ";".join(self.mail_list)
 
    puretext = MIMEText(''+self.mail_content)
    msg.attach(puretext)
    xlsxpart = MIMEApplication(open('F:/jenkins_workspace/workspace/youtime/report/example_requests.csv', 'rb').read())
    xlsxpart.add_header('Content-Disposition', 'attachment', filename='example_requests.csv')
    msg.attach(xlsxpart)
    try:
      s = smtplib.SMTP_SSL() #创建邮件服务器对象
      s.connect(self.mail_host) #连接到指定的smtp服务器。参数分别表示smpt主机和端口
      s.login(self.mail_user, self.mail_pass) #登录到你邮箱
      s.sendmail(me, self.mail_list, msg.as_string()) #发送内容
      s.close()
      return True
    except Exception:
      return False
 
 
if __name__ == '__main__':
  #send list
  mailto_list = ["748862180@qq.com"] #邮件接收人
  mail_title = '紧急!youtime测试反馈,请及时查看'
  mail_content = 'youtime测试报告出现请求失败!!!'
  mm = Mailer(mailto_list,mail_title,mail_content)
  res = mm.sendMail()
  print("发送成功")