import re
import scrapy
from scrapy_splash import SplashRequest


class HhSpiderSpider(scrapy.Spider):
    name = 'hh_spider'
    allowed_domains = ['hh.kz']
    # start_urls = ['http://hh.kz/']

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
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        yield SplashRequest(url="https://hh.kz/vacancy/43021761?query=python",
                            callback=self.parse,
                            endpoint='execute',
                            args={
                                'lua_source': self.lua_script
                            },
                            headers=headers)

    def parse(self, response):
        print(response.body)
        # title = response.css('div.vacancy-title>h1>span: text').get()
        # company = response.css('a.vacancy-company-name>span>span: text').get()
        # money = response.css('p.vacancy-salary>span: text').get()
        # skills = [tag.css('span: text').get() for tag in response.css('div.bloko-tag-list>div>div')]
        # pattern = r'\d+\s\w+\s\d+'
        # published_date = re.search(pattern, response.css('p.vacancy-creation-time: text').get()).group[0]

        # yield {
        #     'title': title,
        #     'company': company,
        #     'money': money,
        #     'skills': skills,
        #     'published_date': published_date,            
        # }
