# coding: utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
import threading
import config
import requests
import random
import pymongo
import time
import re

#配置数据库
cilent=pymongo.MongoClient(config.MONGO_URL)
db=cilent[config.MONGO_DB]


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# 设置中文
chrome_options.add_argument('lang=zh_CN.UTF-8')
#添加useragent
ua=UserAgent()
user_agent=ua.random
string='user-agent="'+ua.random+'"'
chrome_options.add_argument(string)


#不显示图片，加快加载速度
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

#添加代理
#r = requests.get('http://127.0.0.1:5010/get_all/').content
#PROXY = random.choice(r)
# PROXY=requests.get('http://127.0.0.1:5010/get/').content
# desired_capabilities = chrome_options.to_capabilities()
# desired_capabilities['proxy'] = {
#     "httpProxy": PROXY,
#     "ftpProxy": PROXY,
#     "sslProxy": PROXY,
#     "noProxy": None,
#     "proxyType": "MANUAL",
#     "class": "org.openqa.selenium.Proxy",
#     "autodetect": False
# }
#,desired_capabilities=desired_capabilities

browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 10)

THREAD_NUM = 50


def search(q):
	print('Searching！')
	try:
		browser.get(config.URL)
		showAll = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#reviews-medley-footer > div.a-row.a-spacing-large > a'))
		)
		page_num=pq(browser.page_source).find('#reviews-medley-footer > div.a-row.a-spacing-large > a').text()
		num=re.findall(r'\d+', page_num)
		showAll.click()
		browser.switch_to_window(browser.window_handles[1])
		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#cm_cr-review_list ')))
		get_comments(q)
		return num[0]
	except TimeoutException:
		get_comments(q)


def next_page(pagenum,q):
	print('正在翻页！')
	try:
		next = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#cm_cr-pagination_bar > ul > li.a-last'))
		)
		next.click()
		wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#filter-info-section > span'), str(pagenum*10+1)))
		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#cm_cr-review_list .review.aok-relative')))
		get_comments(q)
	except TimeoutException:
		next_page(pagenum,q)


def get_comments(q):
	try:
		html = browser.page_source
		doc = pq(html)
		doc.xhtml_to_html()
		roots = doc('#cm_cr-review_list .review.aok-relative').items()
		#f = open("comment.txt","a",encoding='UTF-8')
		for item in roots:
			star = item.find('.a-link-normal').attr('title')
			score = int(star[0])
			if score > 3:
				score = 1
			else:
				score = 0
			'''
			comment = {
				'score': score,
				'comment': item.find('.review-title.a-color-base.review-title-content.a-text-bold > span').text()+','+item.find('.review-data > span > span').text()
			}
			'''
			comment = item.find('.review-title.a-color-base.review-title-content.a-text-bold > span').text()+','+item.find('.review-data > span > span').text()
			string_com_old_1 = comment[1:-1]
			if not (bool(re.search(r'\\u', string_com_old_1, flags= 2)) or bool(re.search(r'video', string_com_old_1, flags= 2))):
                            string_com_old_2 = re.sub(r'\\u003c', "<", string_com_old_1)
                            string_com_old_3 = re.sub(r'\\u003e', ">", string_com_old_2)
                            string_com_old_4 = re.sub(r'\\u0026', "&", string_com_old_3)
                            string = re.sub(r'\\n', "", string_com_old_4)
			try:
                                #print(string)
                                q.put(string)
				#print(comment)
				#f.write(str(comment))
				#f.write("\n")
			#save_to_mongo(comment)
			except UnicodeEncodeError:
				print("UnicodeEncodeError!!!")
	except TimeoutException:
		print('Get comments time out!')

def set_url(url):
	config.URL = url


def set_brand(brand):
	config.Brand = brand


def main(q):
	page_num = int(int(search(q))/10)+1
	print(page_num)
	for i in range(1, page_num):
		next_page(i,q)
	browser.get('https://httpbin.org/headers')
	browser.close()
	q.put(None)

def crawler(url):
	set_url(url)
	page_num = int(int(search(q))/10)+1
	print(page_num)
	for i in range(1, page_num):
		next_page(i)
	browser.get('https://httpbin.org/headers')
	browser.close()

if __name__=='__main__':
	main()
