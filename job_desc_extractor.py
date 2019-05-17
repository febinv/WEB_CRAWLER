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
job_url="https://app.joinhandshake.com/jobs/1244124?ref=web-app-job-search"
data=pd.read_csv("/Users/Febin/Desktop/Research/handshake_1.csv")
data['1']=data['1'].fillna(0)
final_data=pd.DataFrame()
data_final=[]
for row in data.itertuples():
    # try
    job_contact_nm=[]
    job_contact_title=[]
    job_sal=[]
    job_desc=[]
    if data.loc[row.Index,'1']!=0:
        base_page=driver.get(data.loc[row.Index,'1'])
        time.sleep(10)
        pagetext = driver.execute_script("return document.body.innerHTML")
        html_source=driver.page_source
        soup = BeautifulSoup(html_source,"html.parser")
        time.sleep(1)
        prefix="https://arizona.joinhandshake.com"
        results = soup.findAll("div",class_="style__card___2_7Ix")
        if soup.find("div",class_="style__cover___EcB_L style__card___2_7Ix"):
            results_money= soup.find("div",class_="style__cover___EcB_L style__card___2_7Ix")
            resultsm_1 = results_money.find("div",class_="style__card-item___1KHjT style__card-item-body___n6-om")
            resultsm_2 = resultsm_1.find("div",class_="style__media-body___1QdtR")
            resultsm_3=  resultsm_2.find("div",class_="style__feature-group___3nwCu")
            for results_m in resultsm_3.findAll("div",class_="style__feature-group-item___2fiTu"):
                try:
                    if results_m.find("i",class_="fa icon fa-money"):
                        job_sal=results_m.find("i",class_="fa icon fa-money").next_sibling
                except:
                    pass

        for results_1 in results:
            try:
                results1 = results_1.find("div",class_="style__job-description___17MNY")
                results2 = results1.find("div",class_="style__card-item___1KHjT style__card-item-body___n6-om")
                results3=  results2.find("div",class_="style__transition___2UjAT")
                if results3.findAll("p"):
                    for results_2 in results3.findAll("p"):
                        job_desc.append(results_2.text)
                else:
                    job_desc.append(results3.text)
            except:
                pass
        results_recruiter=soup.find("div",class_="col-md-4")
        if soup.find("div",class_="col-md-4"):
            for results_r1 in results_recruiter.findAll("div",attrs={'data-hook' : 'card'},class_="style__card___2_7Ix"):
                for results_r2 in results_r1.findAll("div",class_="style__card-item___1KHjT style__card-item-body___n6-om"):
                    try:
                        if results_r2.find("div",class_=None):
                            job_contact_nm=results_r2.find("div",class_=None).text
                            job_contact_title=results_r2.find("div",class_=None).next_sibling.text
                        else:
                            pass
                    except:
                        pass
        print('1')
        data_final.append([data.loc[row.Index,'1']]+[job_desc]+[job_sal]+[job_contact_nm]+[job_contact_title])
        print(data_final)
    else:
        data_final.append([data.loc[row.Index,'1']])
    # except:
    #     print('c')
    #     data_final.append([data.loc[row.Index,'1']])
    #     pass
final_data=final_data.append(data_final)
final_data.to_csv("handshake_2.csv",encoding='utf-8')