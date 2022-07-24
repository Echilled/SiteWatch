import logging
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup, SoupStrainer
from helpers import is_url_valid, get_clean_url, is_link_internal
import re

logging.basicConfig(
    filename='log.txt',
    filemode='a',
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO
)


class Crawler:

    def __init__(self, url, depth=25):
        self.crawled_urls = set()
        if is_url_valid(url):
            url = get_clean_url(url, '')
            self.depth = depth
            self.index = 0
            self.crawled_urls.add(url)
            self.list = self.crawl(url)

    def get_urllist(self):
        return self.list

    def crawl(self, url):
        '''
        Crawl over URLs
            - scrape for anchor tags with hrefs in a webpage
            - reject if unwanted or cleanup the obtained links
            - append to a set to remove duplicates
            - "crawled_urls" is the repository for crawled URLs
        @input:
            url: URL to be scraped
        '''
        found_urls = []
        try:
            log_file = open("errorlogs.txt", "a+")
            page = urlopen(Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
                }
            ))

            content = page.read()

            soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer(['a', 'link']))
            for anchor in soup.find_all(['a', 'link']):
                link = anchor.get('href')
                if is_url_valid(link):
                    # Complete relative URLs
                    link = get_clean_url(url, link)
                    if is_link_internal(link, url):
                        found_urls.append(link)

            soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer(['script', 'img']))
            for anchor in soup.find_all(['script', 'img']):
                link = anchor.get('src')
                if is_url_valid(link):
                    # Complete relative URLs
                    link = get_clean_url(url, link)
                    if is_link_internal(link, url):
                        found_urls.append(link)

        except HTTPError as e:
            log_file.write('HTTPError:' + str(e.code) + ' in ' + url)
        except URLError as e:
            log_file.write('URLError: ' + str(e.reason) + ' in ' + url)
        except Exception:
            import traceback
            log_file.write('Generic exception: ' + traceback.format_exc() + ' in ' + url)

        log_file.close()
        cleaned_found_urls = set(found_urls)  # To remove repitions
        self.crawled_urls |= cleaned_found_urls  # Union of sets
        # if (len(self.crawled_urls) > self.depth):
        # self.crawled_urls = self.crawled_urls[:self.depth]
        # return
        # else:
        # Crawl the crawled urls
        self.index += 1
        regex = re.compile(
            r'^.*\.(?!js$|ico$|atom$|png$|ttf$|css$)[^.]+$')  # remove non-webpages
        filtered = sorted([i for i in self.crawled_urls if regex.match(i)])

        print(filtered)
        if self.index < len(filtered):
            url = filtered[self.index]
            self.crawl(url)
            logging.info(f'Crawling: {url}')

        else:
            return
        return filtered


#if __name__ == '__main__':
#    Crawler('https://plainvanilla.com.sg/')
