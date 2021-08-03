from selenium_webTest1 import SeleniumWeb
import configparser
import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json

import pandas as pd


PATH = r"C:\Users\Gurinder\Desktop\Vector\chromedriver.exe"
file = 'thales.scraper.config'
config = configparser.ConfigParser()
config.read(file)
configfile = config['DEFAULT']

if config.has_option("DEFAULT", 'url') :
    url = configfile['url']
else:
    print("No URL Specified")
    exit()

driver = webdriver.Chrome(PATH)
driver.get(url)
print("Let the website load for 10 seconds")
time.sleep(12)
selenium_obj = SeleniumWeb(driver)

if config.has_option("DEFAULT", 'buttons') :
    buttons = configfile['buttons'].split("|")
    selenium_obj.plugin_buttons(buttons)

if config.has_option("DEFAULT", 'keyword'):
    if config.has_option("DEFAULT", 'search_bar'):
        keyword = configfile['keyword']
        searchbar = configfile['search_bar']
        selenium_obj.search_keyword(keyword, searchbar)
    else:
        print("Searching field bar is not specified!! Please check your config file once :)")
        exit()
if 'workday' in url:

    if config.has_option("DEFAULT", 'right_click') and config.has_option("DEFAULT", 'links') and config.has_option("DEFAULT", 'url_selector'):

        links = configfile['links']
        right_click = configfile['right_click']
        url_selector = configfile['url_selector']
        job_links = selenium_obj.retrieve_links_by_right_click(links, right_click, url_selector)
        selenium_obj.get_job_data(job_links, configfile['title'], configfile['description'], configfile)
    else:
        print("Can't fetch Job URLs, please give instructions for right click to select the URL for the particular posting")

else:

    links = configfile['links']
    link_url = selenium_obj.retrieve_links_directly(links)
    selenium_obj.get_job_data(link_url, configfile['title'], configfile['description'], configfile)