import requests
from bs4 import BeautifulSoup,SoupStrainer
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from lxml import html
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ssl
import time
import os
import re
ssl._create_default_https_context = ssl._create_unverified_context
count=50
driver = webdriver.Chrome()
final_data=pd.DataFrame()
url_login="https://arizona.joinhandshake.com/login"
page = driver.get(url_login)
driver.find_element_by_xpath("//*[@id='main']/div[1]/div[2]/div[2]/a/div[2]").click()
time.sleep(1)
elem=driver.find_element_by_id("username")
elem.send_keys("febinv")
time.sleep(1)
elem=driver.find_element_by_id("password")
elem.send_keys("")
driver.find_element_by_xpath("//*[@id='left_col']/div[2]/input[4]").click()
time.sleep(3)
driver.find_element_by_xpath("//*[@id='radio_push']").click()
time.sleep(5)
driver.find_element_by_xpath("//*[@id='left_col']/div[2]/input").click()
time.sleep(15)
#job_url="https://arizona.joinhandshake.com/employers/16761"
data=pd.read_csv("/Users/Febin/Desktop/Research/handshake.csv")
final_data=pd.DataFrame()
data_final=[]
for row in data.itertuples():
    try:
        base_page=driver.get(data.loc[row.Index,'0'])
        time.sleep(10)
        pagetext = driver.execute_script("return document.body.innerHTML")
        html_source=driver.page_source
        soup = BeautifulSoup(html_source,"html.parser")
        time.sleep(1)
        prefix="https://arizona.joinhandshake.com"
        company_job_url=[]
        job_title=[]
        ind_job_url=[]
        app_date=[]
        job_type=[]
        job_locs=[]
        results = soup.findAll("div",class_="style__card___2_7Ix")
        for results_1 in results:
            try:
                results1 = results_1.find("div",class_="style__card-item___1KHjT style__card-item-body___n6-om")
                results2=  results1.find("div",class_=None)
                results3= results2.find('a', {'href': True}, text='View All Jobs')
                if results2.find('a', {'href': True}, text='View All Jobs'):
                    company_job_url=prefix+results3['href']
            except:
                pass
        base_page1=driver.get(company_job_url)
        time.sleep(10)
        pagetext1 = driver.execute_script("return document.body.innerHTML")
        html_source1=driver.page_source
        soup1 = BeautifulSoup(html_source1,"html.parser")
        time.sleep(1)
        results_ind_postings = soup1.findAll("div",class_="col-md-9")
        for elem_0 in results_ind_postings:
                for elem_1 in elem_0.findAll("div",class_="style__media-body___1QdtR"):
                    for elem_2 in elem_1.findAll("div",class_="style__flex___2v4Zi style__align-center___DtZP- style__justify-space-between___UzIiu"):
                        ind_job_url=prefix+elem_2.a["href"]
                        job_title=elem_2.div.get_text()
                        # print(ind_job_url)
                        # print(job_title)
                    for elem_3 in elem_1.findAll("div",class_="style__flex___2v4Zi"):
                        for elem_4 in elem_3.findAll("div",class_="style__flex-item___1e-YW"):
                                for elem_4_1 in elem_4.findAll("div",class_="style__feature___2fAvg"):
                                    if elem_4_1.find("i",class_="fa icon style__icon___1lUgT fa-briefcase fa-fw"):
                                        job_type=elem_4_1.find("i",class_="fa icon style__icon___1lUgT fa-briefcase fa-fw").next_sibling
                                        # print(job_type)
                                    if elem_4_1.find("div",{'title':True}):
                                        job_locs= elem_4_1.find("div",attrs={"class":"style__list-with-tooltip___2c5rW"})["title"]
                                        # print(job_locs)
                                    if elem_4_1.span:
                                        app_date=elem_4_1.span.get_text()
                                        # print(app_date)
                    data_final.append([data.loc[row.Index,'0']]+[ind_job_url]+[job_title]+[job_type]+[job_locs]+[app_date])
    except:
        data_final.append([data.loc[row.Index,'0']])
        pass
final_data=final_data.append(data_final)
print(final_data)
final_data.to_csv("handshake_1.csv")





