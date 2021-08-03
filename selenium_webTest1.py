import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json

import pandas as pd


PATH = r"C:\Users\Gurinder\Desktop\Vector\chromedriver.exe"

class SeleniumWeb:

    column_names = ["company", "url", "location", "title", "description"]
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

        job_links = self.driver.find_elements_by_xpath(links)

        job_urls = []
        action = ActionChains(self.driver)

        counter = 30

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
            print(title)
            #location = self.driver.find_element_by_xpath("//div[@title = 'Toronto, Ontario']")
            #location = location.text
            description = self.driver.find_element_by_xpath(desc).get_attribute("outerHTML")
            print(description)
            self.driver.back()
            #print(location)
            time.sleep(3)
            time.sleep(5)

    def retrieve_links_directly(self, link_url):

        links = self.driver.find_elements_by_xpath(link_url)
        job_links = []
        for link in links:
            job_links.append(link.get_attribute('href'))
            print(link.get_attribute('href'))
        return job_links








