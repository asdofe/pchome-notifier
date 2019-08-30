#coding=utf-8
import os
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from urllib import urlopen
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  

 
#url - the url to fetch dynamic content from.
#delay - second for web view to wait
#block_name - id of the tag to be loaded as criteria for page loaded state.
def fetchHtmlForThePage(url, delay, block_name):
    #supply the local path of web driver.
    #in this example we use chrome driver
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument('--disable-gpu')
    opts.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    opts.add_argument("user-agent=Firefox Gecko")
    browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=opts)
    #open the browser with the URL
    #a browser windows will appear for a little while
    browser.get(url)
    try:
    #check for presence of the element you're looking for
        element_present = EC.presence_of_element_located((By.ID, block_name))
        WebDriverWait(browser, delay).until(element_present)
 
    #unless found, catch the exception
    except TimeoutException:
        print "Loading took too much time!"
 
    #grab the rendered HTML
    html = browser.page_source
    #close the browser
    browser.quit()
    #return html
    return html

last_price = 0
cur_price = 0

def write_file(fn, content):
	with open(fn, 'a') as f:
		f.write(content)

while True:
	html_doc = fetchHtmlForThePage('https://24h.pchome.com.tw/prod/DRAF01-A9007KK0I?fq=/S/DRAF01', 60, 'PriceTotal')
	soup = BeautifulSoup(html_doc, 'html.parser')
	cur_price =soup.find(id='PriceTotal').decode_contents(formatter="html")
	if last_price > cur_price:
		break
	last_price = cur_price
	time.sleep (1)
	ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	write_file('price.csv',  ts + ',' +last_price + '\n')

write_file('price.csv', 'price low %u \n'%(last_price))


