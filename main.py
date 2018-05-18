if __name__ == '__main__':
    
    from crawler import Crawler

    crawler = Crawler()

    crawler.to_csv(crawler.extract_product_info(crawler.filter_urls(crawler.crawl("https://www.epocacosmeticos.com.br/"))))