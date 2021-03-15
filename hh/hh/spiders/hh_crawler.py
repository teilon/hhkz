import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class HhCrawlerSpider(CrawlSpider):
    name = 'hh_crawler'
    allowed_domains = ['hh.kz']
    start_urls = ['https://hh.kz/search/vacancy?area=160&fromSearchLine=true&st=searchVacancy&text=python']

    rules = (
        Rule(LinkExtractor(restrict_css=r'span.g-user-content>a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css=r'div.pager-block>a'), follow=True),
    )

    def parse_item(self, response):
        title = ''
        company = ''
        money = ''
        skills = []
        date_of_published = ''
