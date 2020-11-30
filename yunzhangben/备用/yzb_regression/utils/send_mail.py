import smtplib
from email.mime.text import MIMEText
from email.header import Header


class SendMail:
    
    def __init__(self, mail_host):
        self.mail_host = mail_host


    def send(self, title, content, sender, auth_code, receivers):
        message = MIMEText(content, "html", "utf-8")
        message["From"] = "{}".format(sender)
        message["To"] = ",".join(receivers)
        message["Subject"] = title
        try:
            smtp_obj = smtplib.SMTP_SSL(self.mail_host, 465) #启用ssl发信，端口一般是465
            smtp_obj.login(sender, auth_code) #登录
            smtp_obj.sendmail(sender, receivers, message.as_string())
            print("Email 发送成功！")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    mail = SendMail("smtp.qq.com")   #邮件服务器地址
    sender = "748862180@qq.com"        #邮件发送人
    receivers = ["1640464937@qq.com"]  #邮件接收人
    title = "云账本测试报告"
    content = """
        云账本app测试结果
    """
    auth_code = "mjeigilwlzvxbcfg" #临时授权码
    mail.send(title, content, sender, auth_code, receivers)
    