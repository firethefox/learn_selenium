#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on 2019/6/15

@author: laiyu
'''

from time import sleep
from selenium import webdriver
from PIL import Image,ImageEnhance
from aip import AipOcr
#引入百度AI，帐号密码
import sys
sys.path.append("C:\\Users\\laiyu\\eclipse-workspace")
from my import APP_ID,API_KEY,SECRET_KEY,phonenum,password
# 初始化文字识别
aipOcr=AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_auth_code(driver,codeEelement):
    '''获取验证码'''
    driver.save_screenshot('E:\\login\\login.png')  #截取登录页面
    imgSize = codeEelement.size   #获取验证码图片的大小
    imgLocation = imgElement.location #获取验证码元素坐标
    rangle = (int(imgLocation['x']),int(imgLocation['y']),int(imgLocation['x'] + imgSize['width']),int(imgLocation['y']+imgSize['height']))  #计算验证码整体坐标
    login = Image.open('E:\\login\\login.png')  
    frame4=login.crop(rangle)   #截取验证码图片
    imgry = frame4.convert('L')  # 图像加强，二值化
    sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save("E:\\login\\authcode.png")  # 将处理后的图片，保存为new.png
    # 读取图片
    filePath = "E:\\login\\authcode.png"

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # 定义参数变量
    options = {'language_type':'ENG'}

    # 网络图片文字文字识别接口
    result = aipOcr.webImage(get_file_content(filePath),options)
    print(result)
    try:
        authCodeText = result['words_result'][0]['words']
        authCodeText = authCodeText.replace(' ','')
        authCodeText = authCodeText.replace('(','c')
        authCodeText = authCodeText.replace(')','j')
        authCodeText = authCodeText.replace('/','j')
        authCodeText = authCodeText.replace('!','j')
    except:
        return 'a'
    print(authCodeText)
    return authCodeText

#     authcodeImg = Image.open('E:\\login\\authcode.png')
#     authCodeText = image_to_string(authcodeImg,config="--psm 7").strip()

driver = webdriver.Firefox()
# driver.set_window_size(480, 800)
driver.maximize_window()
driver.get('http://www.189.cn/sc/')
driver.implicitly_wait(5)
# driver.switch_to_frame("topLoginFrame")
now_window = driver.current_window_handle
driver.find_element_by_xpath("//*[text()='自助服务']").click()
# driver.switch_to_default_content()
sleep(3)
all_window = driver.window_handles
for handle in all_window:
    if handle != now_window:
        driver.switch_to_window(handle)
sleep(2)
driver.find_element_by_xpath("//input[@id='txtAccount']").click()
driver.find_element_by_xpath("//input[@id='txtAccount']").clear()
driver.find_element_by_xpath("//input[@id='txtAccount']").send_keys(phonenum)
sleep(1)
for i in range(5):
    driver.find_element_by_xpath("//input[@id='txtShowPwd']").click()
    driver.find_element_by_xpath("//input[@id='txtPassword']").clear()
    driver.find_element_by_xpath("//input[@id='txtPassword']").send_keys(password)
    imgElement = driver.find_element_by_xpath("//img[@id='imgCaptcha']")
    authCodeText = get_auth_code(driver,imgElement)
    n = 1
    while len(authCodeText) != 4 or (not authCodeText.encode('utf-8').isalnum()):
        driver.find_element_by_xpath("//img[@id='imgCaptcha']").click()
        print('更换验证码%d次' % n)
        n+=1
        sleep(2)
        authCodeText = get_auth_code(driver,imgElement)           
    driver.find_element_by_xpath("//input[@id='txtCaptcha']").send_keys(authCodeText)
    driver.find_element_by_xpath("//a[@id='loginbtn']").click()
    sleep(2)
    try:
        if "我的收货地址" in  driver.find_element_by_xpath("/html/body/div[15]/div[2]/div[1]/div[2]/table/tbody/tr[2]/th").text:
            print('登录成功！')
            break        
    except:
        print('验证码错误%s次' % (i+1))
        if i == 4:
            driver.quit()
sleep(3)
driver.find_element_by_xpath("//div[text()='积分服务' and @style='display: block']").click()
driver.find_element_by_xpath("//*[text()='签到/查询/兑换']").click()
sleep(5)
driver.switch_to_frame("bodyIframe")
sleep(2)
driver.find_element_by_xpath("//*[@id='current_qdljf']").click()
print("签到成功！")
# 接受警告框
sleep(2)
driver.switch_to_alert().accept()