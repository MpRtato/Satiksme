from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.headless = False
driver = uc.Chrome(use_subprocess=True,options=options)

URL = 'https://saraksti.rigassatiksme.lv/index.html#tram/1/a-b'
driver.get(URL)
driver.implicitly_wait(10)
box = driver.find_element(By.XPATH,"//*[@id='divScheduleContentInner']/table[1]/tbody[2]/tr[2]/td/a[1]")
boxtt=driver.find_element(By.XPATH,"//*[@id='divScheduleContentInner']/table[1]/tbody[2]/tr[2]").text
boxt=driver.find_element(By.XPATH,"//*[@id='divScheduleContentInner']/table[1]/tbody[2]/tr[2]/td").text
box.click()

b=list(boxt)

boxtt.split()
print(boxtt[0])

numl=[]
l=0
i = 0
ii = 1
while l<len(b)/2:
    num=b[i]+b[ii]
    numl.append(num)
    i=i+2
    ii=ii+2
    l=l+1
print(numl)

a=0
a=input('>')