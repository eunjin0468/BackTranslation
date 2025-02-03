import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import pandas as pd

import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import tqdm
from tqdm import tnrange
from urllib.request import urlopen
import re
import requests
import urllib.request
from tqdm import tqdm
import re
import unicodedata

json_file_ko="back_translation_KO.json"
json_file_cn="back_translation_CN.json"
json_file_jp="back_translation_JP.json"
json_file_ru="back_translation_RU.json"

dataset={}

file_path = "TRAM_training_dataset.json"
with open(file_path) as f:
        data = json.load(f)
train_data = pd.json_normalize(data)  
    
text = train_data['text']
label = train_data['technique_id']
driver = webdriver.Chrome(executable_path=r'C:\Python\Python310\chromedriver.exe')
driver.maximize_window()

trans_list = [] 
backtrans_list = [] 
data_list = []

html=driver.page_source
soup=BeautifulSoup(html, 'html.parser')

def trans_to_ko(transed_list, transed_lang): #영어-한글-영어
        for i in tqdm(range(len(transed_list))):
                dataset[text[i]] = []
                trans_list.clear()
                data_list.clear()
                backtrans_list.clear()
                try:
                        try:
                               
                                driver.get('https://papago.naver.com/?sk='+transed_lang+'&tk=ko&st='+transed_list[i])
                                dataset[text[i]] = []
                                time.sleep(2.5)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=ko&tk=en&st='+backtrans)
                                time.sleep(2.5) 
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = {"tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_ko, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                        except:
                                trans_list.clear()
                                data_list.clear()
                                backtrans_list.clear()
                                driver.get('https://papago.naver.com/?sk=en&tk=ko')
                                driver.find_element_by_xpath('//*[@id="txtSource"]/span').send_keys(transed_list[i])
                                time.sleep(2.5)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=ko&tk=en')
                                driver.find_element_by_xpath('//*[@id="txtSource"]/span').send_keys(backtrans)
                                time.sleep(2.5)
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_ko, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                                pass
                        
                except: #특수문자가 들어갔을 경우
                        try: #중간이 특수문자일경우
                                driver.get('https://papago.naver.com/?sk=en&tk=ko')
                                driver.find_element_by_xpath('//*[@id="txtSource"]').send_keys(transed_list[i])
                                time.sleep(4)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=ko&tk=en')
                                driver.find_element_by_xpath('//*[@id="txtSource"]').send_keys(backtrans)
                                time.sleep(4)
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = {"tec_id" : label[i],  "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_ko, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                        except: #맨 앞이 특수문자일 경우
                                try:
                                        transed_list[i]= re.sub('[-=+,#/\^$@*\※~&%ㆍ!』\\\\‘dl…》]','', transed_list[i])
                                        driver.get('https://papago.naver.com/?sk=en&tk=ko')
                                        driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label').send_keys(transed_list[i])
                                        time.sleep(5)
                                        backtrans = driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div/div[2]/div/div[5]/div').text
                                        backtrans_list.append(backtrans)
                                        driver.get('https://papago.naver.com/?sk=ko&tk=en')
                                        driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label').send_keys(backtrans)
                                        time.sleep(5)
                                        data = driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div/div[2]/div/div[5]/div').text 
                                        tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                        dataset[text[i]].append(tec)
                                        with open(json_file_ko, 'w+', encoding='utf_8') as fp:
                                                json.dump(dataset, fp, indent=4, ensure_ascii=False)
                                except:
                                        pass


def trans_to_jp(transed_list, transed_lang): #영어 - 일본어 - 영어
        for i in tqdm(range(len(transed_list))):
                dataset[text[i]] = []
                trans_list.clear()
                data_list.clear()
                backtrans_list.clear()
                try:
                        try:
                                driver.get('https://papago.naver.com/?sk='+transed_lang+'&tk=ja&hn=0&st='+transed_list[i])
                                dataset[text[i]] = []
                                time.sleep(2.5)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=ja&hn=0&tk=en&st='+backtrans)
                                time.sleep(2.5) 
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_jp, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                        except:
                                trans_list.clear()
                                data_list.clear()
                                backtrans_list.clear()
                                driver.get('https://papago.naver.com/?sk=en&tk=ja&hn=0')
                                driver.find_element_by_xpath('//*[@id="txtSource"]/span').send_keys(transed_list[i])
                                time.sleep(2.5)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=ja&hn=0&tk=en')
                                driver.find_element_by_xpath('//*[@id="txtSource"]/span').send_keys(backtrans)
                                time.sleep(2.5)
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = {"tec_id" : label[i],  "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_jp, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                                pass
                        
                except: #특수문자가 들어갔을 경우
                        try: #중간이 특수문자일경우
                                driver.get('https://papago.naver.com/?sk=en&tk=ja&hn=0')
                                driver.find_element_by_xpath('//*[@id="txtSource"]').send_keys(transed_list[i])
                                time.sleep(4)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=ja&hn=0&tk=en')
                                driver.find_element_by_xpath('//*[@id="txtSource"]').send_keys(backtrans)
                                time.sleep(4)
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_jp, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                        except: #맨 앞이 특수문자일 경우
                                try:
                                        transed_list[i]= re.sub('[-=+,#/\^$@*\※~&%ㆍ!』\\\\‘dl…》]','', transed_list[i])
                                        driver.get('https://papago.naver.com/?sk=en&tk=ja&hn=0')
                                        driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label').send_keys(transed_list[i])
                                        time.sleep(5)
                                        backtrans = driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div/div[2]/div/div[5]/div').text
                                        backtrans_list.append(backtrans)
                                        driver.get('https://papago.naver.com/?sk=ja&hn=0&tk=en')
                                        driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label').send_keys(backtrans)
                                        time.sleep(5)
                                        data = driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div/div[2]/div/div[5]/div').text 
                                        tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                        dataset[text[i]].append(tec)
                                        with open(json_file_jp, 'w+', encoding='utf_8') as fp:
                                                json.dump(dataset, fp, indent=4, ensure_ascii=False)
                                except:
                                        pass
                                
                        
                        


def trans_to_cn(transed_list, transed_lang): 
        for i in tqdm(range(len(transed_list))):
                dataset[text[i]] = []
                trans_list.clear()
                data_list.clear()
                backtrans_list.clear()
                try:
                        try:
                               
                                driver.get('https://papago.naver.com/?sk='+transed_lang+'&tk=zh-CN&st='+transed_list[i])
                                dataset[text[i]] = []
                                time.sleep(2.5)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=zh-CN&tk=en&st='+backtrans)
                                time.sleep(2.5) 
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_cn, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                        except:
                                trans_list.clear()
                                data_list.clear()
                                backtrans_list.clear()
                                driver.get('https://papago.naver.com/?sk=en&tk=zh-CN')
                                driver.find_element_by_xpath('//*[@id="txtSource"]/span').send_keys(transed_list[i])
                                time.sleep(2.5)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=zh-CN&tk=en')
                                driver.find_element_by_xpath('//*[@id="txtSource"]/span').send_keys(backtrans)
                                time.sleep(2.5)
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_cn, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                                pass
                        
                except: #특수문자가 들어갔을 경우
                        try: #중간이 특수문자일경우
                                driver.get('https://papago.naver.com/?sk=en&tk=zh-CN')
                                driver.find_element_by_xpath('//*[@id="txtSource"]').send_keys(transed_list[i])
                                time.sleep(4)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=zh-CN&tk=en')
                                driver.find_element_by_xpath('//*[@id="txtSource"]').send_keys(backtrans)
                                time.sleep(4)
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = {"tec_id" : label[i],  "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_cn, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                        except: #맨 앞이 특수문자일 경우
                                try:
                                        transed_list[i]= re.sub('[-=+,#/\^$@*\※~&%ㆍ!』\\\\‘dl…》]','', transed_list[i])
                                        driver.get('https://papago.naver.com/?sk=en&tk=zh-CN')
                                        driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label').send_keys(transed_list[i])
                                        time.sleep(5)
                                        backtrans = driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div/div[2]/div/div[5]/div').text
                                        backtrans_list.append(backtrans)
                                        driver.get('https://papago.naver.com/?sk=zh-CN&tk=en')
                                        driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label').send_keys(backtrans)
                                        time.sleep(5)
                                        data = driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div/div[2]/div/div[5]/div').text 
                                        tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                        dataset[text[i]].append(tec)
                                        with open(json_file_cn, 'w+', encoding='utf_8') as fp:
                                                json.dump(dataset, fp, indent=4, ensure_ascii=False)
                                except:
                                        pass
        

def trans_to_ru(transed_list, transed_lang): 
        for i in tqdm(range(len(transed_list))):
                dataset[text[i]] = []
                trans_list.clear()
                data_list.clear()
                backtrans_list.clear()
                try:
                        try:
                               
                                driver.get('https://papago.naver.com/?sk='+transed_lang+'&tk=ru&st='+transed_list[i])
                                dataset[text[i]] = []
                                time.sleep(2.5)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=ru&tk=en&st='+backtrans)
                                time.sleep(2.5) 
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_ru, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                        except:
                                trans_list.clear()
                                data_list.clear()
                                backtrans_list.clear()
                                driver.get('https://papago.naver.com/?sk=en&tk=ru')
                                driver.find_element_by_xpath('//*[@id="txtSource"]/span').send_keys(transed_list[i])
                                time.sleep(2.5)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=ru&tk=en')
                                driver.find_element_by_xpath('//*[@id="txtSource"]/span').send_keys(backtrans)
                                time.sleep(2.5)
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_ru, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                                pass
                        
                except: #특수문자가 들어갔을 경우
                        try: #중간이 특수문자일경우
                                driver.get('https://papago.naver.com/?sk=en&tk=ru')
                                driver.find_element_by_xpath('//*[@id="txtSource"]').send_keys(transed_list[i])
                                time.sleep(4)
                                backtrans = driver.find_element_by_xpath('//*[@id="txtTarget"]').text
                                backtrans_list.append(backtrans)
                                driver.get('https://papago.naver.com/?sk=ru&tk=en')
                                driver.find_element_by_xpath('//*[@id="txtSource"]').send_keys(backtrans)
                                time.sleep(4)
                                data = driver.find_element_by_xpath('//*[@id="txtTarget"]/span').text 
                                tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                dataset[text[i]].append(tec)
                                with open(json_file_ru, 'w+', encoding='utf_8') as fp:
                                        json.dump(dataset, fp, indent=4, ensure_ascii=False)
                        except: #맨 앞이 특수문자일 경우
                                try:
                                        transed_list[i]= re.sub('[-=+,#/\^$@*\※~&%ㆍ!』\\\\‘dl…》]','', transed_list[i])
                                        driver.get('https://papago.naver.com/?sk=en&tk=ru')
                                        driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label').send_keys(transed_list[i])
                                        time.sleep(5)
                                        backtrans = driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div/div[2]/div/div[5]/div').text
                                        backtrans_list.append(backtrans)
                                        driver.get('https://papago.naver.com/?sk=ru&tk=en')
                                        driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label').send_keys(backtrans)
                                        time.sleep(5)
                                        data = driver.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div/div[2]/div/div[5]/div').text 
                                        tec = { "tec_id" : label[i], "en_text" : transed_list[i], "data_text" : data }
                                        dataset[text[i]].append(tec)
                                        with open(json_file_ru, 'w+', encoding='utf_8') as fp:
                                                json.dump(dataset, fp, indent=4, ensure_ascii=False)
                                except:
                                        pass
trans_to_jp(text, 'en') #영어-일본어-영어
trans_to_cn(text, 'en') #영어-중국어-영어
trans_to_ru(text, 'en') #영어-러시아어-영
trans_to_ko(text, 'en') #영어-한국어-영어
driver.close()
