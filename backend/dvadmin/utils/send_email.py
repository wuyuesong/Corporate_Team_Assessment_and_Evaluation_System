import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header
import base64
import time
 

from conf.env import *
 

def send_email(to_addrs):
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    

    #发送人格式
    #汉字转base64
    fromName64 = base64.b64encode(bytes("考评系统管理员", 'utf-8')) 
    #b'xxxx'转为'xxxx'
    fromName64str = str(fromName64,'utf-8') 
    #尖括号拼接用双引号
    fromNamestr = '"=?utf-8?B?' + fromName64str + '=?=" <' + EMAIL_SENDER + ">"


    smtpobj = smtplib.SMTP_SSL(SMTP_SERVER)  # 创建对象

    failed_list = []
    try:
        # 建立连接--qq邮箱服务和端口号（可百度查询）
        smtpobj.connect(SMTP_SERVER, 465)
        # 登录--发送者账号和口令
        smtpobj.login(EMAIL_SENDER, EMAIL_PASSWORD)
        # 发送邮件
        for to_addr in to_addrs:
            msg = MIMEText(f'''您的公司邀请您参加考评任务\n 
                    以下是您的账号和密码：\n
                    账号：    {to_addr["username"]} \n
                    密码：    {to_addr["password"]} \n
                    ''', 'plain', 'utf-8')
            msg['From'] = Header(fromNamestr)  # 发送者
            subject = '考评任务' # 主题
            msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
            msg['To'] = Header(to_addr["staff_name"])  # 接收者
            time1 = time.time()
            try:
                
                tmp = smtpobj.sendmail(EMAIL_SENDER, to_addr["addr"] , msg.as_string())
                time2 = time.time()
                print("成功时间：", time2-time1)
                print(tmp)
                print(to_addr["addr"])
            except smtplib.SMTPException as e:
                failed_list.append(to_addr)
                print("失败时间：", time.time()-time1)
                
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("无法发送邮件: ", e)
    finally:
        # 关闭服务器
        smtpobj.quit()

    return failed_list