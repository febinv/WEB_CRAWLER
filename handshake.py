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
time.sleep(3)
driver.find_element_by_xpath("//*[@id='left_col']/div[2]/input").click()
time.sleep(10)
job_url="https://arizona.joinhandshake.com/career_fairs/3556/employers_list"
final_data=pd.DataFrame()
base_page=driver.get(job_url)
for i in range(0,7):
    time.sleep(10)
    pagetext = driver.execute_script("return document.body.innerHTML")
    html_source=driver.page_source
    soup = BeautifulSoup(html_source,"html.parser")
    time.sleep(1)
    results = soup.findAll("div",class_="style__card___2_7Ix")
    prefix="https://arizona.joinhandshake.com"
    company_posting_url=[]
    company_title=[]
    company_category=[]
    company_url=[]
    company_desc=[]
    company_calendar=[]
    span_list=[]
    data_final=[]
    for elem in results:
        try:
            company_posting_url=prefix+elem.find("div",class_="style__avatar-container___GPiQn").a["href"]
            company_title=elem.find("div",class_="style__avatar-container___GPiQn").a["title"]
            elem1=elem.find("div",class_="style__media-body___1QdtR")
            for elem2 in elem1.findAll("div",class_="feature-group__feature col-sm-6"):
                if elem2.find("i",class_="fa icon fa-users"):
                    company_category=elem2.find("i",class_="fa icon fa-users").next_sibling
                    print(company_category)
                if elem2.find("i",class_="fa icon fa-link"):
                    company_url=elem2.find("i",class_="fa icon fa-link").next_sibling["href"]
                    print(company_url)
            for elem6 in elem1.findAll("p")[0]:
                if elem6:
                    company_desc=elem6.span.get_text()
                    print(company_desc)
            for elem7 in elem1.find("div",class_="style__sessions-list___36Zjp"):
                if elem7:
                    company_calendar=elem7.text
                    print(company_calendar)
            for elem3 in elem1.find("div",class_="style__details___2hjkQ"):
                for elem4 in elem3.findAll("div",class_="row"):
                    for elem8 in elem4.findAll("div",class_="style__section-header___3Hwm3"):
                        if elem8:
                            span_list.append(elem8.next_sibling)
            job_title=span_list[0]
            job_type=span_list[1]
            employment_type=span_list[2]
            maj_groups=span_list[3]
            work_auth=span_list[4]
            school_year=span_list[5]
            data_final.append([company_posting_url]+[company_title]+[company_category]+[company_url]+[company_desc]+[company_calendar]+[job_title]+[job_type]+[employment_type]+[maj_groups]+[work_auth]+[school_year])
        except:
            pass
    final_data=final_data.append(data_final)
    if i!=6:
        driver.find_element_by_xpath("//*[@id='next-page']").click()
    time.sleep(10)

final_data.to_csv("handshake.csv")






















