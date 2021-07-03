from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
import pandas as pd
config = {'url' : 'https://vectorinstitute.bamboohr.com/jobs/', 'links' : '//div[contains(@itemtype, "http://schema.org/JobPosting")]//div//a'}
driver.get(config['url'])
print(driver.title)
print("Job links found as")
search = driver.find_elements_by_xpath(config['links'])
print(search)
for i in search:
  print(i)
  print(i.get_attribute("href"))
print("Done!")
