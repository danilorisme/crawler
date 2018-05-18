# -*- coding: utf-8 -*-

import re
import csv
import requests
from bs4 import BeautifulSoup

class Crawler(object):
    
    def __init__(self, base_url = None):
        self._base_url = base_url

    def parse_html(self, url):
        content = requests.get(url)
        return BeautifulSoup(content.text, "html.parser")

    def get_urls(self, url):
        page = self.parse_html(url)
        links = set()

        if not self._base_url:
            self._base_url = url

        for tag in page.find_all("a", href=True):
            if tag["href"].startswith(self._base_url):
                links.add(tag["href"])
        return links

    def crawl(self, url):
        self._base_url = url
        seens_urls = set([url])
        available_urls = set([url])

        while available_urls:
            url = available_urls.pop()

            try:
                for link in self.get_urls(url):
                    if link not in seens_urls:
                        seens_urls.add(link)
                        available_urls.add(link)
            except Exception:
                continue

        return seens_urls

    def filter_urls(self, urls, pattern=None):
        if not pattern:
            pattern = r'^https://www\.epocacosmeticos\.com\.br/.+/p$'
        filtered_urls = filter(lambda x: re.search(pattern, x), urls)
        return list(filtered_urls)

    def extract_product_info(self, urls, css_class=None):
        products_info = []

        if not css_class:
            css_class = "productName"

        for url in urls:
            product_page = self.parse_html(url)
 
            product_title = product_page.find("title").string.strip()
            product_name = product_page.find(class_=re.compile(css_class)).string.strip()

            products_info.append([product_title, product_name, url])
            
        return products_info

    def to_csv(self, products):
        with open('output/products.csv', 'w') as csvfile:
            fieldnames = ['title', 'name', 'url']
            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, delimiter=';'
            )
            writer.writeheader()
            for product in products:
                writer.writerow(
                    {
                        'title': product[0],
                        'name': product[1],
                        'url': product[2]
                    }
                )