#!/usr/bin/python
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from message import out
import time
import random
from io import open
import os

def expand_reviews(driver):
	try:
		#button to "Read All Reviews"
		button = driver.find_element_by_xpath('/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[6]/div/span/span')
		#click this button, now we have lots of reviews
		driver.execute_script("arguments[0].click()", button)
		time.sleep(2)
	except:
		print('Read All Reviews button is not found. Might be not enough reviews')

def select_reviews_mode(driver,mode):
	time.sleep(1)
	#click on the type of value from the list you want
	#find the list of review types ('Newest', 'Rating', 'Most Interesting')
	button = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div[1]/div/div[1]/div[1]')
	driver.execute_script("arguments[0].click()", button)
	#expand this list
	time.sleep(1)
	button = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div[1]/div/div[2]/div['+str(mode+1)+']')
	driver.execute_script("arguments[0].click()", button)

def show_more_button(driver):
	try:
		show_more_button = driver.find_element_by_xpath("//*[@id=\"fcxH9b\"]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div")
		driver.execute_script("arguments[0].click()", show_more_button)
		time.sleep(0.25)
	except:
		#if there is no 'show more' button, then we collected all reviews and we stop scrolling
		out('No show more button',False)
		return False
	return True



def load_reviews(driver, url, reviews_amount, ratings, mode,output_file):
	
	#open the app's page
	out("Open "+url+"",False)
	driver.get(url)
	

	expand_reviews(driver)

	select_reviews_mode(driver, mode)

	#load all reviews by scrolling down
	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")
	running=True
	scrolls_happened=0
	folders_analized=0
	filtered_folders_count=0
	while running:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(0.5)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			#try to find and click 'show more' reviews
			running = show_more_button(driver)

		last_height = new_height
		start_time_loading = time.time()

		while True:
			try:
				dr = driver.find_element_by_class_name("Fx1lse")
				if(time.time()-start_time_loading>10):
					break;
			except:
				break
	
		folders_analized,filtered_folders_count = output(driver, output_file,ratings,folders_analized,filtered_folders_count)
		out('[This page] Correct rating reviews: '+str(filtered_folders_count), False)
		out('[This page] Total reviews: '+str(folders_analized),False)

		if (filtered_folders_count>=reviews_amount):
			running=False
			return folders_analized

def output(driver,output_file,ratings,folders_analized,filtered_folders_count):
	#elements consist of reviews (user name, review, rating, data, ect.)
	folder_selenium = driver.find_element_by_xpath('/html/body/div[1]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]').find_elements_by_css_selector('[jsController=H6eOGe]')
	folder = []
	for i in range(len(folder_selenium)):
		if(folders_analized>i):
			continue

		folders_analized+=1
		
		try:
			folder.append(BeautifulSoup(folder_selenium[i].get_attribute('outerHTML'),'lxml'))
		except:
			out('error found and exluded',False)

	#iterate through each folder and get reviews and ratings
	for i in range(len(folder)):
		#if the review is too big then it's truncates by Google. If true then there are two elements with truncated review and full review. We need to get the longest review possible
			
		smallReview = folder[i].find('span', jsname="bN97Pc").text
		fullReview = folder[i].find('span', jsname="fbQN7e").text
		review = ''
		if len(fullReview)==0:
			review = smallReview
		else:
			review = fullReview

		#add out review to the array
		
		#get rating text and add to the array
		rating = folder[i].find('div', class_="pf5lIe").find('div').get('aria-label')
		author = folder[i].find('span', class_="X43Kjb").text
		date = folder[i].find('span', class_="p2TkOb").text
		digit = 0
		for q in range(len(rating)):
			if str(rating[q]).isdigit():
				digit = int(rating[q])
				break

		if(ratings==1 & int(digit)>=4 or ratings==0 & int(digit)==3 or ratings==-1 & int(digit)<=2):
			filtered_folders_count+=1


		#info = str(digit)+"[-]"+author+"[-]"+date+"[-]"+review
		info = str(digit)+" "+review
		info = info.replace("\r","")
		info = info.replace("\n","")
		output_file.write(info+'\n')
		output_file.flush()
	return folders_analized,filtered_folders_count
