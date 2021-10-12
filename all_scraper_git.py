from selenium_webTest1 import SeleniumWeb
import configparser
import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import xml.etree.ElementTree as xml
import xml.etree.ElementTree as xml1
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import pandas as pd

#Intializing the webdriver for selenium
options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')

import pandas as pd


def createXML_Separate(filename):

    filePATH = os.listdir("config/")

    
    prefix = "config/"
    filelist = [prefix + filename + ".csv"]
    
    root = xml.Element('items')
    tree = xml.ElementTree(root)

    for csv in filelist:

        df = pd.read_csv(csv)
        n = df.shape[0]
        for i in range(n):
            jobXml = Element('item')
            root.append(jobXml)
            jobTitle = xml.SubElement(jobXml, 'title')
            jobTitle.text = df.iloc[i]['title']

            description = xml.SubElement(jobXml, 'description')
            description.text = df.iloc[i]['description']

            url = xml.SubElement(jobXml, 'url')
            url.text = df.iloc[i]['url']

            img_job = xml.SubElement(jobXml, 'logo')
            img_job.text = df.iloc[i]['logo']

            company = xml.SubElement(jobXml, 'company')
            company.text = df.iloc[i]['company']

    separate_xml = filename + ".xml"
    file_obj = open(separate_xml, "wb+")
    file_obj.write(str(xml1.tostring(root))[2:-1].encode('utf-8'))

    print("Done!")

def createXML(mergedlist):

    filelist = mergedlist
    print(filelist, "Files to be merged")

    root = xml.Element('items')
    tree = xml.ElementTree(root)

    for csv in filelist:

        df = pd.read_csv(csv)
        n = df.shape[0]
        for i in range(n):
            jobXml = Element('item')
            root.append(jobXml)
            jobTitle = xml.SubElement(jobXml, 'title')
            jobTitle.text = df.iloc[i]['title']

            description = xml.SubElement(jobXml, 'description')
            description.text = df.iloc[i]['description']

            url = xml.SubElement(jobXml, 'url')
            url.text = df.iloc[i]['url']

            img_job = xml.SubElement(jobXml, 'logo')
            img_job.text = df.iloc[i]['logo']

            company = xml.SubElement(jobXml, 'company')
            company.text = df.iloc[i]['company']

    file_obj = open("merged.xml", "wb+")
    file_obj.write(str(xml1.tostring(root))[2:-1].encode('utf-8'))

    print("Done!")

filelist = os.listdir("config/src/src")
print("companies to be scraped :: ", filelist)

separate_list = []
merged_list = []
company_log = []
status_company = []

for file in filelist:
    try:
        config = configparser.ConfigParser()
        file = "config/src/src/" + file
        config.read(file)
        configfile = config['DEFAULT']

        if config.has_option("DEFAULT", 'url') :
            url = configfile['url']
        else:
            print("No URL Specified")
            continue

        driver.get(url)
        print("Let the website load for 10 seconds")
        time.sleep(12)
        selenium_obj = SeleniumWeb(driver)
        
        if config.has_option("DEFAULT", 'UTM_Source Code') :
            utm = configfile['UTM_Source Code']
        else:
            utm = ""

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
                selenium_obj.get_job_data(job_links, configfile['title'], configfile['description'], configfile, utm)
            else:
                print("Can't fetch Job URLs, please give instructions for right click to select the URL for the particular posting")

        else:

            links = configfile['links']
            link_url = selenium_obj.retrieve_links_directly(links)
            selenium_obj.get_job_data(link_url, configfile['title'], configfile['description'], configfile, utm)

        filename = "config/" + configfile['company'] + ".csv"
        selenium_obj.df.to_csv(filename)
        
        if configfile['separate_url'] == "True":
            createXML_Separate(configfile['company'])
        else:
            merged_list.append(filename)
            
        createXML(merged_list)

        print("Job parsing for  ",configfile['company'], " done successfully!!")
        company_log.append(configfile['company'])
        status_company.append("Successful")
        
    except:
        print("Cant Scrape for ", configfile['company'], ", ....... skipping !!!")
        company_log.append(configfile['company'])
        status_company.append("Fail")
        
stats = {'Company' : company_log, 'Status' : status_company}
df_status = pd.DataFrame(data = stats)
df_status.to_csv("Status_log.csv")
        
