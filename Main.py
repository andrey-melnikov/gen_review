#!/usr/bin/python
from gen import load_reviews
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
import sys
import time
from io import open
import os
import datetime
import sys
from celery import Celery

def app_exists(soup):
	#if the app exists in the Google
	try:
		soup.find('h1', class_='AHFaub').span.text
	except:
		sys.exit('App with this id is not found')

def check_id(target_id):
	if target_id=='':
		sys.exit('Search box is null')

	#if user accidentally adds the whole url to input we break the program
	if 'https://play.google.com/store/apps/details?id=' in target_id:
		sys.exit("Do not use the whole URL, use id (ex: com.Company.Appname) instead")

def similar_apps_count(id_):
	check_id(id_)
	url = 'https://play.google.com/store/apps/details?id='+id_
	soup = BeautifulSoup(requests.get(url).text,'lxml')
	try:
		similar_folders = (soup.find('div', jscontroller="i2u2Pb")).findAll('div',class_="wXUyZd")
	except:
		similar_folders=[]
	return len(similar_folders)

def get_source_similar_apps_ids(soup):
	similar_folders = (soup.find('div', jscontroller="i2u2Pb")).findAll('div',class_="wXUyZd")
	dic =[]
	for i in range(len(similar_folders)):
		dic.append(similar_folders[i].findChild().get('href').replace('/store/apps/details?id=',''))
	print('Returned similar apps to the native app')
	return list(dict.fromkeys(dic))#remove doubles. Dictionary removes doubles automatically

def manually_add_ids(ids):
	for i in range(len(ids)):
		check_id(ids[i])
		url = 'https://play.google.com/store/apps/details?id='+target_id
		soup = BeautifulSoup(requests.get(url).text,'lxml')
		app_exists(soup)
	return ids


def launch_driver():
	isHomeComputer=False

	if isHomeComputer:
		geckodriver_path = '/home/andrey/PYTHON_PROJECTS/Reviews_Parser/gen_review/geckodriver'
	else:
		geckodriver_path='/usr/local/bin/geckodriver'
	#launch a browser
	driver_options = webdriver.FirefoxOptions()
	driver_options.add_argument('--headless')

	#proxy_file = [line.rstrip('\n') for line in open('proxy_file')]
	#proxy_server_address = ""
	#port_number = 0

	profile = webdriver.FirefoxProfile()
	
	
	try:
		connected = False
		while(connected==False):
			try:
				#proxy_index = random.randint(0, len(proxy_file) - 1)
				#proxy_server_address = proxy_file[proxy_index].split(':')[0]
				#port_number = proxy_file[proxy_index].split(':')[1]

				#profile.set_preference("network.proxy.type", 1)
				#profile.set_preference("network.proxy.http", proxy_server_address)
				#profile.set_preference("network.proxy.http_port", int(port_number))
				#profile.update_preferences()

				driver = webdriver.Firefox(executable_path=geckodriver_path, firefox_options = driver_options)
				print('Open Browser')
				connected=True
			except:
				connected=False
	except:
		sys.exit('Something went wrong with the Web Browser. Try again later')
		return

	return driver


def main(target_id, lang, reviews_amount, ratings, mode_t, output_name, similar_ids):
	#check the format of the target_id
	check_id(target_id)
	#create a url of the target app
	url = 'https://play.google.com/store/apps/details?id='+target_id+'&gl=us&hl='+lang
	#get the static content of the target app's page
	soup = BeautifulSoup(requests.get(url).text,'lxml')
	#check if app with target_id exists
	app_exists(soup)

	#create and open for writing the output file for reviews
	output_path = "output/reviews/"+output_name+".txt"
	output_file = open(output_path, 'w+',encoding='utf-8')

	if len(similar_ids)==0:
		#get similar app's ids
		similar_ids = get_source_similar_apps_ids(soup)
	else:
		#else we already filled similar_ids manually 
		pass

	#lauch a driver
	driver = launch_driver()

	EXTRA_TARGET_REVIEWS=10

	total_reviews = 0
	#get reviews from all similar app's pages
	for i in range(len(similar_ids)):
		#url of a similar app
		url = 'https://play.google.com/store/apps/details?id='+similar_ids[i]+'&gl=us&hl='+lang
		#parse reviews
		if(mode_t=="Long"):
			mode = 2
		else:
			mode = 0
		total_reviews+= load_reviews(driver, url, reviews_amount, ratings, mode, output_file)	


	print('Reviews have been parsed successfully')
	print('Total number of reviews: '+str(total_reviews))
	#close the browser
	driver.quit()
	#close the output file
	output_file.close()
	print('Web Browser is closed')



if __name__ =="__main__":
	target_id = "com.ansangha.drjb"
	lang = "en-US"
	reviews_amount = 200
	ratings = 1
	mode = "Short"
	output_name = str(datetime.datetime.now())
	
	if similar_apps_exist(target_id):
		auto=True
		similar_ids=[]
	else:
		#fill maually
		auto=False
		similar_ids=[]

	main(target_id,lang, reviews_amount, ratings, mode, output_name, similar_ids)
