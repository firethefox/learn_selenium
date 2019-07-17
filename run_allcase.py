#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on 2019年7月17日

@author: laiyu
'''

import unittest
import os
import time
from HTMLTestRunner import HTMLTestRunner
# 用例路径
case_path = os.path.join(os.getcwd(), "mycase")
# 报告存放路径
report_path = os.path.join(os.getcwd(), "report")
def all_case():
    testsuite = unittest.defaultTestLoader.discover(case_path,pattern="test*.py",top_level_dir=None)
    print(testsuite)
    return testsuite
def getNowtime():
    '''获取当前系统时间'''
    return time.strftime('%Y-%m-%d %H_%M_%S',time.localtime(time.time()))

if __name__ == "__main__":
#     runner = unittest.TextTestRunner()
    myreport = os.path.join(report_path,getNowtime()+'report.html')
    fp=open(myreport,'wb')
    runner = HTMLTestRunner(stream=fp,title='自动化测试报告,测试结果如下：',description='用例执行情况：')
    runner.run(all_case())