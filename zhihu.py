# coding=utf-8
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
# 用Chrome浏览器打开
driver=webdriver.Chrome()
# 打开网址
driver.get(url="http://www.zhihu.com")
time.sleep(2)
# 找到登陆按钮并点击
driver.find_element_by_css_selector('a[href="#signin"]').click()
time.sleep(2)
# 找到输入框并输入账号
driver.find_element_by_name("account").send_keys("zh")
time.sleep(2)
driver.find_element_by_name("password").send_keys("passwd")
time.sleep(2)
# 手动输入验证码
yzm=input("")
driver.find_element_by_name("captcha").send_keys(yzm)
# 点击登陆按钮登陆
driver.find_element_by_css_selector('div.button-wrapper.command > button').click()
# 登陆到要进入的目标页面，登陆的是python话题动态页面
cookie=driver.get_cookies()
time.sleep(3)
driver.get(url="https://www.zhihu.com/topic/19552832/hot")
time.sleep(5)
# 实现将滚轮滑倒页面最下方
def execute_times(times):
    for i in range(times+1):

        js="window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(js)
        time.sleep(5)
execute_times(100)
# 解析网页
html=driver.page_source
soup1=BeautifulSoup(html,'lxml')
authors=soup1.select('a.author-link')
# 答主ID名
authors_alls=[]
# 答主主页地址
authors_hrefs=[]
for author in authors:
    authors_alls.append(author.get_text())
    authors_hrefs.append('http://www.zhihu.com'+author.get('href'))
# 答主简介
authors_intros_urls=soup1.find_all('span',class_='bio')
authors_intros=[]
for authors_intros_url in authors_intros_urls:
    authors_intros.append(authors_intros_url.get_text())
csvfile=open('知乎答主信息.csv','w+',encoding='utf-8')
for authors_all,authors_href,authors_intro in zip(authors_alls,authors_hrefs,authors_intros):
    data=[authors_all,authors_href,authors_intro]
    writer=csv.writer(csvfile)
    writer.writerow(data)
