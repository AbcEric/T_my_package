                           Python工具包
                           ***************

Eric_Toolkit为常用工具箱, 包含__init__.py文件指明为module，在c:\anaconda3\envs\tf21-py37环境下打包，其它程序用import引入后即可使用。

一、安装
python setup.py sdist：生成dist文件夹，生成xxx.tar.gz文件，
安装：
用tar -zxvf命令将tar.gz文件解压得到py文件，以及PKG-INFO文件（模块信息），执行python setup.py install安装。或者下载源码后，直接执行python setup.py install或在Linux下sudo python3 setup.py生成模块module


二、使用
from Eric_Toolkit import tk ==> from eToolkit import tk

三、功能
1. tk.py：Python的常用操作，包括日志类Log，
2. Add: class Device()对终端设备的常用操作：包括运行状态等；