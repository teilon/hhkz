import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
from scrapy.spiders import CrawlSpider, Rule


class HhCrawlerSpider(CrawlSpider):
    name = 'hh_crawler'
    allowed_domains = ['hh.kz']
    # start_urls = ['https://hh.kz/search/vacancy?area=160&fromSearchLine=true&st=searchVacancy&text=python']

    lua_script = '''
        function main(splash, args)
            url = args.url  
            assert(splash:go(url))
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    def start_requests(self):      
        yield SplashRequest(
            url='https://hh.kz/search/vacancy?area=160&fromSearchLine=true&st=searchVacancy&text=python',
            endpoint='execute',
            args={
                'lua_source': self.lua_script,
                'wait': 15,
                },
            )

    rules = (
        Rule(LinkExtractor(restrict_css=r'span.g-user-content>a'), callback='parse_item', follow=True, process_request='use_splash'),
        Rule(LinkExtractor(restrict_css=r'div.pager-block>a'), follow=True),
    )

    def use_splash(self, request):
        request.meta['splash'] = {
                'endpoint':'execute',
                'args':{
                    'lua_source': self.lua_script
                    }
                }
        return request

    def parse_item(self, response):
        title = response.css('div.vacancy-title>h1>span: text').get()
        company = response.css('a.vacancy-company-name>span>span: text').get()
        money = response.css('p.vacancy-salary>span: text').get()
        skills = [tag.css('span: text').get() for tag in response.css('div.bloko-tag-list>div>div')]
        pattern = r'\d+\s\w+\s\d+'
        published_date = re.search(pattern, response.css('p.vacancy-creation-time: text').get()).group[0]

        yield {
            'title': title,
            'company': company,
            'money': money,
            'skills': skills,
            'published_date': published_date,            
        }