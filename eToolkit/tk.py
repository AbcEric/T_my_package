# -*- Coding: utf-8 -*-

"""
File: etk.py

This Python 3 code is one of Eric's toolkit used to define and simplity log operation

Author:     Eric Lee
Date:	    2020/7/10
Version     1.0.2
License:    ABC

History:    1. 2020-07-09: Add Log class first;
            2. Add Device class;
            3. 2020-07-29：Send eMail class：

"""

import logging
import uuid
import socket
import time
import psutil
import platform
import os
import smtplib              # 用于邮件发送
from email.mime.text import MIMEText
from email.header import Header

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "[%Y-%m-%d %H:%M:%S]"

# 日志记录级别：DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50)
DEBUG = 10
INFO = 20
ERROR = 40


# 采用QQ邮箱进行邮件发送
# QQ邮箱默认关闭SMTP服务，需要登录邮箱开启，并生成授权码: 用绑定手机发送短信“配置邮件客户端”到1069070069
class Mail:
    # 发信方的信息：发信邮箱，QQ邮箱授权码, 收信邮箱，邮件服务器
    def __init__(self, from_addr, passwd, to_addr, smtp_server='smtp.qq.com'):
        self.from_addr = from_addr
        self.to_addr = to_addr

        # 开启发信服务，这里使用的是加密传输
        try:
            self.server = smtplib.SMTP_SSL(smtp_server)
            self.server.connect(smtp_server, 465)

            # 登录发信邮箱
            self.server.login(from_addr, passwd)
        except Exception as e:
            print("登录邮箱失败[{0}:{1}:{2}]：{3}".format(from_addr, passwd, smtp_server, str(e)))
            self.server = None

        return

    def sendmail(self, subject, text, msg_format='plain', msg_coding='utf-8', close=False):
        if self.server is None:
            print("请先登录你的邮箱 ...")
            return

        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(text, msg_format, msg_coding)

        # 邮件头信息
        msg['From'] = Header(self.from_addr)
        msg['To'] = Header(self.to_addr)
        msg['Subject'] = Header(subject)

        # 发送邮件
        self.server.sendmail(self.from_addr, self.to_addr, msg.as_string())

        # 关闭服务器
        if close:
            self.server.quit()
        return


# 个人的日志记录：
class Log:
    # osd: 控制是否同步在桌面终端显示，缺省不显示, 用于调试！
    # 若在debug中增加osd=参数，由于print没有采用args和kwargs方式，只能采用"xxx{0}{1}.format(x1, x2)"的方式传参
    def __init__(self, logfile, loglevel, osd=False):
        # 日志记录函数初始化：
        logging.basicConfig(filename=logfile, level=loglevel, format=LOG_FORMAT, datefmt=DATE_FORMAT)
        self.osd = osd

        return

    def debug(self, msg, osd=False, *args, **kwargs):
        logging.debug(msg, *args, **kwargs)
        # 只要osd任一个为True，则同步打印到桌面：注意只能采用format方式
        if self.osd or osd:
            print(msg, *args, **kwargs)

    def info(self, msg, osd=False, *args, **kwargs):
        logging.info(msg, *args, **kwargs)
        if self.osd or osd:
            print(msg, *args, **kwargs)

    def error(self, msg, osd=False, *args, **kwargs):
        logging.error(msg, *args, **kwargs)
        if self.osd or osd:
            print(msg, *args, **kwargs)


# 取计算机、raspi等终端设备的信息：
class Device:
    # 取Mac地址：
    def get_mac(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

    # 获取本机IP：在raspi下主机名对应的IP为127.0.0.1，取wlan0对应的IP
    # def get_ip(self):
    #     my_name = self.get_hostname()
    #     my_addr = socket.gethostbyname(my_name)
    #     return my_addr

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            # ('xxx.xxx.xxx.xxx', port number)
            ip = s.getsockname()

        except Exception as e:
            print("get_ip error: ", str(e))
            return ""

        finally:
            s.close()
            return ip[0]

    # 获取本机电脑名：
    def get_hostname(self):
        my_name = socket.getfqdn(socket.gethostname())
        return my_name

    # 取本机日期：YYYY-MM-DD
    def get_date(self):
        r_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        return r_date

    # 取本机时间：HH:MM:SS
    def get_time(self):
        r_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        return r_time

    # 取本机总内存和已使用内存：单位为M
    def get_memory(self):
        phy_mem = psutil.virtual_memory()
        total = round(phy_mem.total / 1024 / 1024)
        used = round(phy_mem.used / 1024 / 1024)
        return total, used

    # 取CPU使用率，缺省取样1秒钟：
    def get_cpu(self, time_count=1):
        r_cpu_total = psutil.cpu_percent(time_count, 0)
        r_cpu_eachone = psutil.cpu_percent(time_count, 1)
        return r_cpu_total, r_cpu_eachone

    # 取CPU温度：
    def get_temperature(self):
        if platform.system() == "Windows":
            return "Unknown"

        # temperature = os.popen('cat /sys/class/thermal/thermal_zone0/temp').read()
        temperature = os.popen('vcgencmd measure_temp').read()
        # temperature带“temp=”
        r_temp = temperature[5:-1]
        return r_temp


if __name__ == '__main__':
    '''
    qqmail = Mail("xxx@qq.com", "ifseaywpkzlkbcfi", "lihuachun@abchina.com")
    # 不加close可连续发送：
    qqmail.sendmail("You are welcome!", "Hi, this is a email send by QQ. 用于自动发送的测试", close=True)
    '''

    dev = Device()
    print(dev.get_mac(), dev.get_hostname())
    print(dev.get_date(), dev.get_time())
    print(dev.get_memory())
    print(dev.get_ip())
    print(dev.get_cpu())
    print(dev.get_temperature())
