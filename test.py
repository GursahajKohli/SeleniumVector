from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

#Intializing the webdriver for selenium
options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')

def parse_job(link, config, job_details,  job_csv, column_names):
  print("Parsing job at url  :: ", link) 
  
  driver.get(link)
  
  job_title = driver.find_element_by_xpath(job_details['title'])
  
  job_location = driver.find_element_by_xpath(job_details['location'])
  
  job_description = driver.find_element_by_xpath(job_details['description'])
  
  job_logo = job_details['logo']
  
  job_company = config['company']
  
  if 'reference' in job_details.keys():
    job_reference = driver.find_element_by_xpath(job_details['reference'])
  else:
    job_reference = link
    
  remote_fetcher = str(job_location).split()
  
  for i in remote_fetcher :
    if i.lower() == 'remote':
      job_remote = 'True'
      break
    else:
      job_remote = 'False'
  
  job_url = link
  
  job_list = [job_company, '<html><body>' + str(job_description) + '</body></html>', job_location, job_logo, job_reference, job_remote, job_title, job_url]
  df2 = pd.DataFrame(job_list)
  df2 = df2.transpose()
  print(df2.shape, "#1")
  print(job_csv.shape, "#2")
  
  job_csv = job_csv.append(df2)
  print("Job fetched from ::", link)
  return(job_csv)
  

#Config & job data, will be fetched in future from config files
config = {'url' : 'https://vectorinstitute.bamboohr.com/jobs/', 'links' : '//div[contains(@itemtype, "http://schema.org/JobPosting")]//div//a', 'company' : 'Vector Institute'}
job_details = {'title' : '//div[contains(@class, "col-xs-12 col-sm-8 col-md-12")]//h2', 'location' : '//span[contains(@class, "ResAts__card-subtitle")]', 'description' : '//div[contains(@class, "col-xs-12 BambooRichText")]', 'logo' : 'https://images3.bamboohr.com/93316/logos/cropped.jpg?v=29'}
column_names = ['company', 'description', 'location', 'logo', 'reference', 'remote', 'title', 'url']

job_csv = pd.DataFrame(columns = column_names)
#final_csv = pd.DataFrame()
#Start fetching 
driver.get(config['url'])
print(driver.title)
print("Job links found as")
search = driver.find_elements_by_xpath(config['links'])
print(search)
for i in search:
  print(i)
  print(i.get_attribute("href"))
  link = i.get_attribute("href")
  job_csv = parse_job(link, config, job_details, job_csv, column_names)
  
job_csv.to_csv('Jobs.csv')
  

  
 
