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
"""

import logging
import uuid
import socket
import time
import psutil
import platform
import os

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "[%Y-%m-%d %H:%M:%S]"

# 日志记录级别：DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50)
DEBUG = 10
INFO = 20
ERROR = 40


# 个人的日志记录
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
    dev = Device()
    print(dev.get_mac(), dev.get_hostname())
    print(dev.get_date(), dev.get_time())
    print(dev.get_memory())
    print(dev.get_ip())
    print(dev.get_cpu())
    print(dev.get_temperature())
