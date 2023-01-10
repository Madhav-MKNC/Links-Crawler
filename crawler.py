#!/usr/bin/env python3

"""
# Title:    AAVE Docs Scraper
# author:   MKNC (https://github.com/Madhav-MKNC)
# created:  09-01-2023 22:50 
"""

# AAVE docs link
# url = "https://docs.aave.com/hub/"

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls = urls

    def get_url_content(self, url):
        return requests.get(url).text

    def scrape_all_urls(self, url):
        soup = BeautifulSoup(self.get_url_content(url), 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if not path.startswith('http'):
                path = urljoin(url,path)
            if path not in self.urls and path not in self.visited_urls:
                self.urls.append(path)

    def crawl(self):
        try:
            while self.urls:
                url = self.urls.pop(0)
                print("[+] Crawling:",url)
                try:
                    self.scrape_all_urls(url)
                    self.visited_urls.append(url)
                except AttributeError:
                    print(f'[-] No href on : {url}\n')
                except Exception as e:
                    print(f'[!] Failed to crawl: {url}')
                    print("[!] REASON:",e,'\n')
        except KeyboardInterrupt:
                print("[-] Program Exited...")


if __name__ == '__main__':
    import platform
    import os 

    os.system('cls' if 'win' in platform.uname().system.lower() else 'clear')
    print("LINKS CRAWLER\n")

    url = input('[=] Enter the base url you want to crawl: ')
    # url = "https://docs.aave.com/hub/"
    if not url.startswith('https://'): url = 'https://'+url

    aave = Crawler(urls=[url])
    aave.crawl()
    print("len(urls) =",len(aave.urls))
    print("len(set(urls)) =",len(set(aave.urls)))
    with open('links_crawled.txt','w') as f:
        f.write("\n".join(aave.visited_urls))
    print("[+] list saved in 'links_crawled.txt'")
