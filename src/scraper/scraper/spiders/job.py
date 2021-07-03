import configparser
import re

import scrapy
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
from tqdm import tqdm

from ..items import JobDetails
from ..helpers import PaginationConfigOption

MOUSECLICK = None
with open('./scraper/scripts/mouseclick.lua') as f:
    MOUSECLICK = f.read()

DEBUG_PAGELIMIT = 1

# hard limit on number of jobs to scrape
JOBLIMIT = 30

PAGE_DELAY_SECONDS = 10

REMOTE_LOCATION_RE = re.compile('remote|virtual', re.IGNORECASE)

BLOCKED_HTML_TAGS = ['img']


class JobSpider(scrapy.Spider):
    """
    Extracts job urls from job list, and job details from each url.
    """
    name = 'job'

    def __init__(self, **kwargs):
        config = configparser.ConfigParser()
        config.read(kwargs['config'])
        self._config = config['DEFAULT']

        self._debug = kwargs['debug']
        self._page_counter = 0
        self._job_counter = 0

        self._progress_bar = tqdm()

    def start_requests(self):
        # TODO: add support for multiple URLs (e.g. jobs and internships)
        yield SplashRequest(url=self._config['url'],
                            callback=self.parse_list,
                            args={'wait': PAGE_DELAY_SECONDS},
                            dont_filter=False)

    def parse_list(self, response):
        self._page_counter += 1

        print(f'Parsing job list: {response.url}')
        joblinks = response.xpath(self._config['joblist.link.xpath'])
        print(f'Found {len(joblinks)} job links.')

        # TODO: this works ok if we only have 1 page,
        # need to adjust for > 1 page (e.g. using list of pbars?)
        self._progress_bar = tqdm(total=min(len(joblinks), JOBLIMIT))

        for job in joblinks:
            job_url = job.xpath('./@href').get()

            if self._job_counter < JOBLIMIT:
                self._job_counter += 1
                yield SplashRequest(url=response.urljoin(job_url),
                                    callback=self.parse_details,
                                    args={'wait': PAGE_DELAY_SECONDS},
                                    dont_filter=False)

            else:
                print(f'Hit job limit of {JOBLIMIT}, not scraping any more URLs...')
                return

        pagination_type = PaginationConfigOption[self._config.get('joblist.pagination')]
        
        # TODO: add support for infinite scroll
        if pagination_type != PaginationConfigOption.NONE:
            # generate CSS selector for next page and pass to SplashRequest
            nextpage_selector = None

            if pagination_type == PaginationConfigOption.NEXTPAGE:
                nextpage_selector = self._config['joblist.nextpage.css']
            elif pagination_type == PaginationConfigOption.PAGENUMBER:
                nextpage_selector = self._config['joblist.nextpage.css'] \
                    .replace('$PAGENUMBER', str(self._page_counter + 1))

            # if DEBUG, make sure we haven't exceeded out page limit,
            # otherwise navigate to next page
            if not self._debug or self._page_counter < DEBUG_PAGELIMIT:
                print(f'Requesting next page...')
                yield SplashRequest(url=response.url,
                                    callback=self.parse_list,
                                    endpoint='execute',
                                    args={
                                        'lua_source': MOUSECLICK,
                                        'selector': nextpage_selector
                                    },
                                    dont_filter=False)

    def parse_details(self, response):
        print(f'Parsing job details: {response.url}')

        try:
            title = response.xpath(
                self._config['jobdetails.title.xpath']).get().strip()

            company = self._config['company_name']

            location = '; '.join(
                response.xpath(
                    self._config['jobdetails.location.xpath']).getall()).strip()
            
            location = location.replace(';', '')

            description = \
                ''.join(
                    response.xpath(
                        self._config['jobdetails.description.xpath']).getall()) \
                .replace('\n', '')
            description = self._clean_html_description(description)

            url, email, reference = None, None, None
            if self._config.getboolean('jobdetails.is_url_application'):
                url = response.url
                reference = url

                utm_params = self._config.get('jobdetails.url_utm_params')
                # append UTM params to URL if present in config
                if utm_params and utm_params != str(None):
                    url = url + utm_params
            else:  # use email instead
                email = self._config['jobdetails.application_email']

            category = None
            if 'jobdetails.category.xpath' in self._config:
                category = response.xpath(
                    self._config['jobdetails.category.xpath']).get().strip()

            # mark job as remote in XML, if location contains text like "remote" or "virtual"
            remote = None
            if re.search(REMOTE_LOCATION_RE, location):
                remote = True

            # populate logo url from config, if present
            logo = None
            if 'jobdetails.logo' in self._config:
                logo = self._config['jobdetails.logo']

            # TODO: posting date, job type (?)

            # create job details object
            yield JobDetails(title=title,
                            company=company,
                            location=location,
                            description=description,
                            url=url,
                            email=email,
                            category=category,
                            remote=remote,
                            logo=logo,
                            reference=reference)

        except AttributeError as e:
            print(f'Failed to scrape job ({response.url}), skipping...')
            print(f'Error detail: {e}')

        finally:
            self._progress_bar.update()

    def _clean_html_description(self, description):
        """
        Returns a copy of description with all blocked tags (e.g. <img>) removed.
        """
        soup = BeautifulSoup(description, 'lxml')

        for tag in BLOCKED_HTML_TAGS:
            results = soup.find_all(tag)

            for result in results:
                if not result.decomposed: result.decompose()

        return str(soup)
