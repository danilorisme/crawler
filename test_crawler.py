import re
import requests
from bs4 import BeautifulSoup
import unittest
import crawler
from crawler import Crawler


class TestCrawler(unittest.TestCase):
    
    def setUp(self):
        self.crawler = Crawler()

    def test_parse_html(self):
        parsed_html = self.crawler.parse_html("http://localhost:8080/store/")
        self.assertIsInstance(parsed_html, BeautifulSoup)

    def test_get_urls(self):
        test_url = "http://localhost:8080/store/"
        expected_urls = [
            "http://localhost:8080/store/product1.html",
            "http://localhost:8080/store/product2.html"
        ]
        page_urls = self.crawler.get_urls(test_url)

        self.assertTrue(all(url in expected_urls for url in page_urls))

    def test_extract_product_info(self):
        test_urls = [
            "http://localhost:8080/store/product1.html",
            "http://localhost:8080/store/product2.html"
        ]
        expected_product_info = [
            ['Product 1', 'Product 1', 'http://localhost:8080/store/product1.html'],
            ['Product 2', 'Product 2', 'http://localhost:8080/store/product2.html']
        ]
        teste_css_class = "product-name"
        extracted_product_info = self.crawler.extract_product_info(test_urls,teste_css_class)

        self.assertTrue(all(product_info in expected_product_info for product_info in extracted_product_info))

    def test_crawl(self):
        test_url = "http://localhost:8080/store"
        expected_urls = [
            "http://localhost:8080/store", 
            "http://localhost:8080/store/product1.html", "http://localhost:8080/store/product2.html",
            "http://localhost:8080/store/product3.html", "http://localhost:8080/store/product4.html",
            "http://localhost:8080/store/product5.html", "http://localhost:8080/store/product6.html"
        ]
        
        site_urls = self.crawler.crawl(test_url)
        
        self.assertTrue(all(url in expected_urls for url in site_urls))

    def test_filter_urls(self):
        test_urls = [
            "http://www.test.com.br/aaaa/p", "http://www.test.com.br/bbbb/p",
            "http://www.test.com.br/p/cccc", "http://www.test.com.br/p/dddd",
            "http://www.test.com.br/p"
        ]
        expected_urls = [
            "http://www.test.com.br/aaaa/p", "http://www.test.com.br/bbbb/p"
        ]
        test_pattern = r'^http://www\.test\.com\.br/.+/p'
        filtered_urls = self.crawler.filter_urls(test_urls, test_pattern)

        self.assertTrue(all(url in expected_urls for url in filtered_urls))
        

if __name__ == '__main__':

    unittest.main()