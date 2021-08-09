import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
import xml.etree.ElementTree as xml
import xml.etree.ElementTree as xml1
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import pandas as pd
import os

class SeleniumWeb:

    column_names = [ "title", "company", "url", "description", "logo"]
    df = pd.DataFrame(columns = column_names)


    def __init__(self, driver):
        self.driver = driver
        print("Selenium started to work")

    def plugin_buttons(self, buttons):

        xpath_button = buttons

        for xpathb in xpath_button:

            selector = self.driver.find_element_by_xpath(xpathb)
            try:
                selector.click()

            except selenium.common.exceptions.ElementNotInteractableException:
                selector.send_keys(Keys.SPACE)
            print("Selection made")
            time.sleep(5)



    def search_keyword(self, keyword, search_bar):

        time.sleep(5)
        search = self.driver.find_element_by_xpath(search_bar)
        print("Searching for keyword :: ", keyword)
        search.send_keys(keyword)
        time.sleep(1)
        search.send_keys(Keys.RETURN)
        print("Search complete!")

    def retrieve_links_by_right_click(self, links, right_click, url_selector):

        print("Retrieving links")
        time.sleep(6)
        print(links)
        job_links = self.driver.find_elements_by_xpath(links)[: -1]
        print(len(job_links))

        job_urls = []
        action = ActionChains(self.driver)

        counter = 5

        for job in job_links:
            if counter < 0:
                break
            counter = counter - 1
            time.sleep(2)
            action = ActionChains(self.driver)
            action.context_click(job).perform()
            element = self.driver.find_element_by_xpath(right_click)
            job_url = element.get_attribute(url_selector)
            job_urls.append(job_url)
            print(job_url)
            element = self.driver.find_element_by_xpath("//body")
            element.send_keys(Keys.ESCAPE)
            print("Next job")
        return(job_urls)

    def get_job_data(self, job_urls, title1, desc, configfile):

        for job in job_urls:

            self.driver.get(job)
            time.sleep(10)
            company_name = configfile['company']
            title = self.driver.find_element_by_xpath(title1)
            title = title.text
            #location = self.driver.find_element_by_xpath("//div[@title = 'Toronto, Ontario']")
            #location = location.text

            description = self.driver.find_element_by_xpath(desc).get_attribute("outerHTML")

            self.driver.back()
            #print(location)
            time.sleep(3)
            time.sleep(5)
            url = job
            logo = configfile['logo']
            self.appendCSV(company_name, description, logo, title, url)
            print("Job ", title, "Scraped successfully!!")


    def appendCSV(self, company, description, logo, title, url):


        description = '<html><body>' + description + '</body></html>'
        df3 = pd.DataFrame({"title" : [title], "company" : [company], "url" : [url],  "description" : [description], "logo"  : [logo]})
        self.df = self.df.append(df3)
    def retrieve_links_directly(self, link_url):


        links = self.driver.find_elements_by_xpath(link_url)
        job_links = []
        for link in links:
            job_links.append(link.get_attribute('href'))
            print(link.get_attribute('href'))
        return job_links

    def createXML(self):

        filelist = os.listdir("config/*.csv")
        prefix = "config/"
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
