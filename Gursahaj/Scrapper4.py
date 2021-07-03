from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as xml
import xml.etree.ElementTree as xml1
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import re

import json

#Integrate AI

r = requests.get('https://boards.greenhouse.io/integrateai')

html = r.text

soup = BeautifulSoup(html, 'html.parser')


child = []
for tag in soup.findAll('div',{'class' : 'opening'}):

    child.append(tag.findChild())
job_board = 'https://boards.greenhouse.io'

job_links = []
for opening in child:
    job_links.append(job_board+opening['href'])


root = xml.Element('jobs')
tree = xml.ElementTree(root)
for jobs in job_links:

    job_request = requests.get(jobs)
    job_html = job_request.text
    job_soup = BeautifulSoup(job_html, 'html.parser')

    for job in job_soup.findAll('div', {'id' : 'content'}):
        #print(job)
        job_title = job_soup.find('h1', {'class' : 'app-title'}).string
        job_location = job_soup.find('div', {'class' : 'location'}).string
        job_content = job_soup.find('div', {'id' : 'content'})
        job_content = '<html><body>' + str(job_content).replace('<div class="" id="content">', '').replace('</div>', '').replace('\n', '') + '</body></html>'
        job_img = job_soup.find('img')['src']
        print(job_content)

        #print("Job title :: ", job_title)
        #print("Job location :: ", job_location)
        #print("Job contents :: ", job_content)


        jobXml = Element('job')
        root.append(jobXml)
        jobTitle = xml.SubElement(jobXml, 'job_title')
        jobTitle.text = job_title
        print(job_title)

        description = xml.SubElement(jobXml, 'description')
        description.text = job_content

        url = xml.SubElement(jobXml, 'url')
        url.text = jobs
        print(url)

        apply_email = xml.SubElement(jobXml, 'apply_email')

        img_job = xml.SubElement(jobXml, 'job_img')
        img_job.text = job_img

        company = xml.SubElement(jobXml, 'company')
        company.text = "integrate.ai"

        company_url = xml.SubElement(jobXml, 'company_url')
        company_url.text = "https://integrate.ai/"

        city = xml.SubElement(jobXml, 'city')
        city.text = str(job_location.strip())

        location = xml.SubElement(jobXml, 'location')
        location.text = "Canada"

        reference = xml.SubElement(jobXml, 'reference')
        #reference.text = "1234"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
r = requests.get('https://layer6.ai/careers/#', headers = headers)

html = r.text

soup = BeautifulSoup(html, 'html.parser')

job_img = soup.find('div', {'class' : 'siteBranding'})
job_img = job_img.findChildren('img')[0]['src']
print(job_img)

jobs = 'https://layer6.ai/careers/#'

for i in soup.findAll('section', {'class' : 'singleJobModal'}):

    job_title = (i.findChildren('h1', {'class' : 'singleJobModal__title'})[0])

    job_title = str(job_title).replace('<h1 class="singleJobModal__title"><p><strong>', '').replace('</strong></p>', '').replace('</h1>', '')[: -1]

    job_location = 'MaRS Discovery District at University & College in Toronto'

    job_content = '<html><body>' + str(i.findChildren('div', {'class' : 'singleJobModal__inner'})[0]) + '</body></html>'

    job_url = jobs + str(i['data-remodal-id'])


    print(job_url)

    jobXml = Element('job')
    root.append(jobXml)
    jobTitle = xml.SubElement(jobXml, 'job_title')
    jobTitle.text = job_title
    print(job_title)

    description = xml.SubElement(jobXml, 'description')
    description.text = job_content.replace('\n', '')

    url = xml.SubElement(jobXml, 'url')
    url.text = job_url
    print(url)

    img_job = xml.SubElement(jobXml, 'job_img')
    img_job.text = 'http://layer6.ai/wp-content/uploads/2018/11/og-image.png'

    apply_email = xml.SubElement(jobXml, 'apply_email')
    apply_email.text = 'careers@layer6.ai'

    company = xml.SubElement(jobXml, 'company')
    company.text = "layer6"

    company_url = xml.SubElement(jobXml, 'company_url')
    company_url.text = "https://layer6.ai/"

    city = xml.SubElement(jobXml, 'city')
    city.text = str(job_location.strip())

    location = xml.SubElement(jobXml, 'location')
    location.text = "Canada"

    reference = xml.SubElement(jobXml, 'reference')
    #reference.text = "1234"

r = requests.get('https://www.canvass.io/careers')
html = r.text

#print(html)

soup = BeautifulSoup(html, 'html.parser')
i = 0
job_links = []
company_link = "https://www.canvass.io"
for tags in soup.findAll('a', {'class' : 'job-listing-card w-inline-block'}):

    job_links.append(company_link + tags['href'])

for jobs in job_links:

    job_request = requests.get(jobs)
    job_html = job_request.text
    job_soup = BeautifulSoup(job_html, 'html.parser')

    job_title = job_soup.find('h1', {'class' : 'page-title-2 section-header'}).string
    job_location = job_soup.find('div', {'class' : 'job-listing-info-text'}).string
    job_content = str(job_soup.find('div', {'class' : 'project-rich-text w-richtext'})).replace("Â", '').replace('â', '').replace('â', "").replace("â¢\t", '').replace('\ ', '').replace("â", '').replace("â", '').replace("t\'s", "t's")
    job_c = job_content.encode("utf-8")

    #print(job_c)

    #job_content = re.sub('Ã¢Â€Â¢\t', '', job_content) .replace('Ã¢Â€Â¢\tWe', 'We').replace('Â·Â Â Â', '').replace('Â', '').replace('â', '').replace('¢\t', '')
    print(job_content)

    job_content = '<html><body>' + job_content + '</body></html>'
    job_img = 'https://global-uploads.webflow.com/6047c01673f666512c81fabf/6048272db932b9fa32c1f6f2_Canvass%20Logo%20RGB%20(1).png'

    jobXml = Element('job')
    root.append(jobXml)

    jobTitle = xml.SubElement(jobXml, 'job_title')
    jobTitle.text = job_title

    description = xml.SubElement(jobXml, 'description')
    description.text = job_content

    url = xml.SubElement(jobXml, 'url')
    url.text = jobs
    print(jobs)

    img_job = xml.SubElement(jobXml, 'job_img')
    img_job.text = job_img

    apply_email = xml.SubElement(jobXml, 'apply_email')
    apply_email.text = 'info@canvass.io'

    company = xml.SubElement(jobXml, 'company')
    company.text = "CANVASS"

    company_url = xml.SubElement(jobXml, 'company_url')
    company_url.text = "https://www.canvass.io/"

    city = xml.SubElement(jobXml, 'city')
    city.text = str(job_location.strip())

    location = xml.SubElement(jobXml, 'location')
    location.text = "Canada"

    reference = xml.SubElement(jobXml, 'reference')


r = requests.get('https://vectorinstitute.bamboohr.com/jobs/')
html = r.text

soup = BeautifulSoup(html, 'html.parser')

for tag in soup.findAll('script', {'id' : 'positionData'}):
    #print(tag.string.split("},{"))
    obj = json.loads(tag.string)

jobs = []
for i in range(0, len(obj)):

    if obj[i]['departmentLabel'] == 'AI Engineering & Technology':
        jobs.append(obj[i])

for job in jobs:

    job_id = job['id']
    link = 'https://vectorinstitute.bamboohr.com/jobs/view.php?id='
    job_link = link + str(job_id)
    r = requests.get(job_link)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    title_scrapper = soup.findAll('div', {'class' : 'ResAts__card-content'})[0]
    description_scrapper = soup.findAll('div', {'class' : 'ResAts__card-content'})[1]

    job_title = title_scrapper.find('h2').string

    job_content = job_content = '<html><body>' + str(description_scrapper) + '</body></html>'

    #print(title_scrapper)
    job_location = soup.find('div', {'class' : 'posInfo__Value'}).string

    job_url = job_link

    job_img = 'https://vectorinstitute.ai/wp-content/uploads/2020/06/logo_uniligual_black_horizontal_trademark.png'

    print(job_img)

    jobXml = Element('job')
    root.append(jobXml)
    jobTitle = xml.SubElement(jobXml, 'job_title')
    jobTitle.text = job_title
    print(job_title)

    description = xml.SubElement(jobXml, 'description')
    description.text = job_content
    print(job_content)

    url = xml.SubElement(jobXml, 'url')
    url.text = job_url
    print(url)

    img_job = xml.SubElement(jobXml, 'job_img')
    img_job.text = job_img

    apply_email = xml.SubElement(jobXml, 'apply_email')
    apply_email.text = 'hr@vectorinstitute.ai'

    company = xml.SubElement(jobXml, 'company')
    company.text = "Vector Institute"

    company_url = xml.SubElement(jobXml, 'company_url')
    company_url.text = "https://vectorinstitute.bamboohr.com/jobs/"

    city = xml.SubElement(jobXml, 'city')
    city.text = str(job_location.strip())

    location = xml.SubElement(jobXml, 'location')
    location.text = "Canada"

    reference = xml.SubElement(jobXml, 'reference')
    #reference.text = "1234"

print(xml1.tostring(root))
file_obj = open("Job_postsLatest.xml", "wb+")
file_obj.write(str(xml1.tostring(root))[2:-1].encode('utf-8'))

print("Done!")


