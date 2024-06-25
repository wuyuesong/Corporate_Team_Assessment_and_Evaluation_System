"""
@author: wuyuesong
@Remark: 邮件发送工具类
"""

# import smtplib
# # email 用于构建邮件内容
# from email.mime.text import MIMEText
# # 构建邮件头
# from email.header import Header
# import base64
# import time
 

# from conf.env import *
 

# def send_email(to_addrs):
#     # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    

#     #发送人格式
#     #汉字转base64
#     fromName64 = base64.b64encode(bytes("考评系统管理员", 'utf-8')) 
#     #b'xxxx'转为'xxxx'
#     fromName64str = str(fromName64,'utf-8') 
#     #尖括号拼接用双引号
#     fromNamestr = '"=?utf-8?B?' + fromName64str + '=?=" <' + EMAIL_SENDER + ">"


#     smtpobj = smtplib.SMTP_SSL(SMTP_SERVER)  # 创建对象

#     failed_list = []
#     try:
#         # 建立连接--qq邮箱服务和端口号（可百度查询）
#         smtpobj.connect(SMTP_SERVER, 465)
#         # 登录--发送者账号和口令
#         smtpobj.login(EMAIL_SENDER, EMAIL_PASSWORD)
#         # 发送邮件
#         for to_addr in to_addrs:
#             msg = MIMEText(f'''您的公司邀请您参加考评任务\n 
#                     以下是您的账号和密码：\n
#                     账号：    {to_addr["username"]} \n
#                     密码：    {to_addr["password"]} \n
#                     ''', 'plain', 'utf-8')
#             msg['From'] = Header(fromNamestr)  # 发送者
#             subject = '考评任务' # 主题
#             msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
#             msg['To'] = Header(to_addr["staff_name"])  # 接收者
#             time1 = time.time()
#             try:
                
#                 tmp = smtpobj.sendmail(EMAIL_SENDER, to_addr["addr"] , msg.as_string())
#                 time2 = time.time()
#                 print("成功时间：", time2-time1)
#                 print(tmp)
#                 print(to_addr["addr"])
#             except smtplib.SMTPException as e:
#                 failed_list.append(to_addr)
#                 print("失败时间：", time.time()-time1)
                
#         print("邮件发送成功")
#     except smtplib.SMTPException as e:
#         print("无法发送邮件: ", e)
#     finally:
#         # 关闭服务器
#         smtpobj.quit()

#     return failed_list



# -*- coding:utf-8 -*-
import smtplib
import email
# import json
# import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from email.mime.base import MIMEBase
# from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr
# import urllib.request
# import ssl
from conf.env import *
import base64
import time
import asyncio

# from celery import Celery, Task
from application.celery import app


# @app.task
# class SendEmailTask(Task):
#     def run(self, to_addrs):
#         send_email(to_addrs)

@app.task
def send_email(to_addrs):
    # username，通过控制台创建的发信地址
    username = EMAIL_SENDER
    # password，通过控制台创建的SMTP密码
    password = EMAIL_PASSWORD
    # # 自定义的回信地址，与控制台设置的无关。邮件推送发信地址不收信，收信人回信时会自动跳转到设置好的回信地址。
    # replyto = 'XXXXXXXX'

    #发送人格式
    #汉字转base64
    fromName64 = base64.b64encode(bytes("考评系统管理员", 'utf-8')) 
    #b'xxxx'转为'xxxx'
    fromName64str = str(fromName64,'utf-8') 
    #尖括号拼接用双引号
    fromNamestr = '"=?utf-8?B?' + fromName64str + '=?=" <' + EMAIL_SENDER + ">"

    # # 显示的To收信地址
    # rcptto = ['address1@example.net', 'address2@example.net']
    # # 显示的Cc收信地址
    # rcptcc = []
    # # Bcc收信地址，密送人不会显示在邮件上，但可以收到邮件
    # rcptbcc = []
    # # 全部收信地址，包含抄送地址，单次发送不能超过60人
    # receivers = rcptto + rcptcc + rcptbcc

    # # 构建alternative结构
    # msg = MIMEMultipart('alternative')
    # msg['Subject'] = Header('自定义信件主题')
    # msg['From'] = formataddr(["自定义发信昵称", username])  # 昵称+发信地址(或代发)
    # # list转为字符串
    # msg['To'] = ",".join(rcptto)
    # msg['Cc'] = ",".join(rcptcc)
    # # msg['Reply-to'] = replyto  #用于接收回复邮件，需要收信方支持标准协议
    # # msg['Return-Path'] = 'test@example.net' #用于接收退信邮件，需要收信方支持标准协议
    # msg['Message-id'] = email.utils.make_msgid() #message-id 用于唯一地标识每一封邮件，其格式需要遵循RFC 5322标准，通常如 <uniquestring@example.com>，其中uniquestring是邮件服务器生成的唯一标识，可能包含时间戳、随机数等信息。
    # msg['Date'] = email.utils.formatdate()

    # # 构建alternative的text/plain部分
    # textplain = MIMEText('自定义TEXT纯文本部分', _subtype='plain', _charset='UTF-8')
    # msg.attach(textplain)

    failed_list = []

    # SMTP普通端口为25或80
    client = smtplib.SMTP('smtpdm.aliyun.com', 80)
    # 开启DEBUG模式
    client.set_debuglevel(0)
    # 发件人和认证地址必须一致
    client.login(username, password)

    start_time = time.time()
    for to_addr in to_addrs:
        msg = MIMEText(f'''您的公司邀请您参加考评任务\n 
                以下是您的账号和密码：\n
                账号：    {to_addr["username"]} \n
                密码：    {to_addr["password"]} \n
                ''', 'plain', 'utf-8')
        msg['From'] = Header(fromNamestr)  # 发送者
        subject = '考评任务-{}-{}'.format(to_addr["staff_name"], to_addr["username"]) # 主题
        msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
        msg['To'] = Header(to_addr["staff_name"])  # 接收者
        receivers = [to_addr["addr"]]
        
        # 发送邮件
        try:
           
            # 备注：若想取到DATA命令返回值,可参考smtplib的sendmail封装方法:
            # 使用SMTP.mail/SMTP.rcpt/SMTP.data方法
            print(receivers)
            ret = client.sendmail(username, receivers, msg.as_string())  # 支持多个收件人，具体数量参考规格清单
            print("ret: ", ret)
            print('邮件发送成功！')
            
            end_time = time.time()
            print("during time: ", end_time - start_time)

        except Exception as e:
            failed_list.append(to_addr)
            print('邮件发送异常, ', str(e))
        
    client.quit()

    return failed_list

