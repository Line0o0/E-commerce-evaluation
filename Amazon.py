# coding: utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
from multiprocessing import Pool
from math import ceil
from time import sleep
import config
import requests
import random
import psutil
import pymongo
import time
import re
import os


#配置数据库
cilent=pymongo.MongoClient(config.MONGO_URL)
db=cilent[config.MONGO_DB]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

# 设置中文
chrome_options.add_argument('lang=zh_CN.UTF-8')
#添加useragent
ua = UserAgent()
user_agent = ua.random
string = 'user-agent="'+ua.random+'"'
chrome_options.add_argument(string)


#不显示图片，加快加载速度
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

#添加代理
r = requests.get('http://127.0.0.1:5010/get_all/').content
PROXY = random.choice(r)
PROXY=requests.get('http://127.0.0.1:5010/get/').content
chrome_options.add_argument('--proxy-server=http://'+PROXY)


browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 15)


def format_url(url):
	print('******Start Searching！*******')
	try:
		browser.get(url)
		id=re.search(r'/dp/B(.*)/ref', url).group(1)
		id_str="".join(id)
		id='B'+id_str
		url='https://www.amazon.cn/product-reviews/'+id+'/?ie=UTF8&pageNumber='
		wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#ags-dp-tips'))
		)
		page_num=pq(browser.page_source).find('#reviews-medley-footer > div.a-row.a-spacing-large > a').text()
		if page_num=='':
			return None
		num = re.findall(r'\d+', page_num)
		if len(num)==0:
			return str(1),url
		if len(num)==1:
			return num[0],url
		if len(num)==2:
			number=num[0]+num[1]
			return number, url
	except TimeoutException:
		print('function format_url time out!')


def assess_link():
	try:
		print('Assessing a link!')
		result = format_url(config.URL)
		if result==None:
			print('This link has no comment!Pass!')
		else:
			page_num = int(ceil(float(result[0]) / 10))
			list = get_stars()#此处拿到各星的统计数据
			url_demo = result[1]
			print('Start Scraping the link!')
			pool = Pool(processes=4)
			for i in range(1, page_num+1):
				print('Scraping comment page ' + str(i))
				url = url_demo+str(i)
				pool.apply_async(get_comments, args=(url, i, ))
		print "Started processes"
		pool.close()
		pool.join()
	except Exception:
		print('Assess a link error!')



def assess_brand():
	try:
		print('Accessing brand!')
		browser.get('https://www.amazon.cn/')
		input = browser.find_element_by_css_selector('#twotabsearchtextbox')
		submit = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#nav-search > form > div.nav-right > div > input')))
		actions = ActionChains(browser)
		actions.move_to_element(input).click().perform()
		actions.move_to_element(input).send_keys(config.Brand).perform()
		submit.click()
		wait.until(
			EC.presence_of_element_located(
				(By.CSS_SELECTOR, '#search > div.sg-row > div.sg-col-20-of-24.sg-col-28-of-32.'
								  'sg-col-16-of-20.sg-col.s-right-column.sg-col-32-of-36.sg-col-8-of-12.'
								  'sg-col-12-of-16.sg-col-24-of-28 > div > span:nth-child(4) > div.s-result-list.'
								  's-search-results.sg-row')))
		html = browser.page_source
		doc = pq(html)
		doc.xhtml_to_html()
		links = []
		roots = doc('#search > div.sg-row > div.sg-col-20-of-24.sg-col-28-of-32.sg-col-16-of-20.sg-col.s-right-column.'
					'sg-col-32-of-36.sg-col-8-of-12.sg-col-12-of-16.sg-col-24-of-28 > div > span:nth-child(4) > div'
					'.s-result-list.s-search-results.sg-row .sg-col-4-of-24.sg-col-4-of-12.sg-col-4-of-36.s-result-item.sg-col-4-of-28.sg-col-4-of-16.sg-col.sg-col-4-of-20.sg-col-4-of-32').items()
		for item in roots:
			descrition = item.find(
				'div > div > div > div:nth-child(2) > div:nth-child(2) > div > div.a-section.a-spacing-none.a-spacing-top-small > h2 > a > span').text()
			if re.search(config.Brand, descrition, re.IGNORECASE):
				com_num = item.find(
					'div > div > div > div:nth-child(2) > div:nth-child(2) > div > div.a-section.a-spacing-none.a-spacing-top-micro > div > a > span').text()
				if com_num != '':
					url = item.find(
						'div > div > div > div:nth-child(2) > div:nth-child(2) > div > div.a-section.a-spacing-none.a-spacing-top-small > h2 > a ').attr(
						'href')
					url = 'https://www.amazon.cn' + url
					links.append(url)
		print('Now have got '+str(len(links)) + ' links!')
		for i in range(0, len(links)):
			print(' ')
			print('Scraping Link No.'+str(i+1)+' !')
			result = format_url(links[i])
			if result==None:
				print('This link has no comment!Pass!')
			else:
				page_num = int(ceil(float(result[0]) / 10))
				url_demo = result[1]
				if page_num<4:
					for i in range(1,page_num+1):
						print('Scraping comment page '+str(i))
						url = url_demo + str(i)
						get_comments(url,i)
				elif page_num>=4:
					pool = Pool(processes=4)
					for i in range(1, page_num+1):
						print('Scraping comment page '+str(i))
						url = url_demo + str(i)
						pool.apply_async(get_comments, args=(url, i,))
					pool.close()
					pool.join()
	except Exception:
		print('Get brand error!')


def get_stars():
	html=pq(browser.page_source)
	# 以下返回的是各个星的评论所占的百分比
	five_stars = html.find('#histogramTable > tbody > tr:nth-child(1) > td.a-span10 > a > div').attr('aria-label')
	four_stars = html.find('#histogramTable > tbody > tr:nth-child(2) > td.a-span10 > a > div').attr('aria-label')
	three_stars = html.find('#histogramTable > tbody > tr:nth-child(3) > td.a-span10 > a > div').attr('aria-label')
	two_stars = html.find('#histogramTable > tbody > tr:nth-child(4) > td.a-span10 > a > div').attr('aria-label')
	one_stars = html.find('#histogramTable > tbody > tr:nth-child(5) > td.a-span10 > a > div').attr('aria-label')

	overall_stars = html.find(
		'.a-fixed-left-grid-col.aok-align-center.a-col-right > div > span > span > a > span').text()[:3]
	total = html.find('#dp-summary-see-all-reviews > h2').text()
	total_obj = re.search(r'(\d?),?(\d*)', total)
	total_num = total_obj.group(1) + total_obj.group(2)
	# 下面这个是总的评论人数
	total_num = str(total_num)
	# 下面这个是综合所有评论的评分
	overall_stars = str(overall_stars)
	#list返回的都是string类型
	list = [total_num, overall_stars, five_stars, four_stars, three_stars, two_stars, one_stars]
	return list


def get_comments(URL, num):
	try:
		list = []
		url=URL
		pagenum = num
		browser.get(url)
		if pagenum <= 100:
			pagenum = str(pagenum * 10 - 10 + 1)
		elif pagenum > 100:
			thousands = int((pagenum*10-10)/1000)
			pagenum = str(thousands) + ',' + str(pagenum * 10 - 9)[-3:]
		wait.until(
			EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#filter-info-section > span'), pagenum))
		html = browser.page_source
		doc = pq(html)
		doc.xhtml_to_html()
		roots = doc('#cm_cr-review_list .review.aok-relative').items()
		comma = '，'.decode('utf-8')
		for item in roots:
			star = item.find('.a-link-normal').attr('title')
			score = int(star[0])
			if score > 3:
				score = 1
			else:
				score = 0
			comment = {
				'score': score,
				'comment': item.find('.review-title.a-color-base.review-title-content.a-text-bold > span').text()+comma+item.find('.review-data > span > span').text()
			}
			list.append(comment)
		save_to_mongo(list)
	except TimeoutException:
		print('Get comments time out!')

def save_to_mongo(result):
	try:
		for i in range(0, len(result)):
			db[config.MONGO_TABLE].insert(result[i])
	except Exception:
		print('存储到数据库失败')



def set_url(url):
	config.URL = url


def set_brand(brand):
	config.Brand = brand

def set_mode(mode):
	config.Mode = mode



def main():
	time1=time.time()
	set_mode('Brand')
	if config.Mode == 'Brand':
		set_brand('puma')
		assess_brand()
	if config.Mode == 'Link':
		set_url('https://www.amazon.cn/dp/B07BX83TPW/ref=sr_1_6?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&keywords=puma&qid=1565770706&s=gateway&sr=8-6')
		assess_link()
	time2 = time.time()
	browser.quit()
	os.system('taskkill /f /im chromedriver.exe')
	os.system('taskkill /f /im chrome.exe ')
	print('takes time ' + str(time2 - time1))
	#print('Useful proxy is '+PROXY)



if __name__=='__main__':
	main()


