import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header
import base64
 

from conf.env import *
 

def send_email(task_name, task_description, username, password, to_addrs):
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    

    #发送人格式
    #汉字转base64
    fromName64 = base64.b64encode(bytes("考评系统管理员", 'utf-8')) 
    #b'xxxx'转为'xxxx'
    fromName64str = str(fromName64,'utf-8') 
    #尖括号拼接用双引号
    fromNamestr = '"=?utf-8?B?' + fromName64str + '=?=" <' + EMAIL_SENDER + ">"


    # 邮件头信息
    msg['From'] = Header(fromNamestr)  # 发送者
    subject = '考评任务' # 主题
    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
    smtpobj = smtplib.SMTP_SSL(SMTP_SERVER)  # 创建对象

    try:
        # 建立连接--qq邮箱服务和端口号（可百度查询）
        smtpobj.connect(SMTP_SERVER, 465)
        # 登录--发送者账号和口令
        smtpobj.login(EMAIL_SENDER, EMAIL_PASSWORD)
        # 发送邮件
        for to_addr in to_addrs:
            msg = MIMEText(f'''您的公司邀请您参加考评任务\n 
                    任务名称：{task_name}\n
                    任务描述：{task_description}\n
                    以下是您的账号和密码：\n
                    账号：    {to_addr["username"]} \n
                    密码：    {to_addr["password"]} \n
                    ''', 'plain', 'utf-8')
            msg['To'] = Header(to_addr["staff_name"])  # 接收者
            smtpobj.sendmail(EMAIL_SENDER, to_addr["addr"] , msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("无法发送邮件: ", e)
    finally:
        # 关闭服务器
        smtpobj.quit()