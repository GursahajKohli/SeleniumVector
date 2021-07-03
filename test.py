import selenium
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://www.techwithtim.net/")
print(driver.title)
print("done")
