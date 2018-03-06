# -*- coding: utf-8 -*-
import scrapy

from scrapy import Request

class SearchAnitubeSpider(scrapy.Spider):
    name = 'search-anitube'
    allowed_domains = ['http://www.anitube.biz']
    start_urls = ['http://www.anitube.biz/?s=Nanatsu no Taizai']

    def __init__(self, search=None, *args, **kwargs):
        super(SearchAnitubeSpider, self).__init__(*args, **kwargs)
        
        if search:
            self.start_urls = ['http://www.anitube.biz/?s=%s' % search]

    def parse(self, response):
        episodes = response.css(".mainBox ul li")
        paginate = response.css(".wp-pagenavi a.page.larger")

        # yield { 'episodes': episodes }

        for episode in episodes:
            name = episode.css('.videoTitle a ::text').extract_first()
            url = episode.css('.videoTitle a ::attr(href)').extract_first()
            thumb = episode.css('.videoThumb a img ::attr(src)').extract_first()

            # yield { 'name': name, 'url': url }

            yield Request(url, callback=self.parse_episode, dont_filter=True, meta={ 'name': name, 'thumb': thumb } )

        if paginate:
            # name_page = paginate.css('a ::text').extract_first()
            url_page = paginate.css('a ::attr(href)').extract_first()

            yield Request(url_page, callback=self.parse_episodes, dont_filter=True )

    def parse_episode(self, response):
        name = response.meta.get('name')
        thumb = response.meta.get('thumb')
        video = response.css(".mainBox video ::attr(src)").extract_first()

        if video:
            yield { 'name': name, 'video': video, 'thumb': thumb }

    def parse_episodes(self, response):
        episodes = response.css(".mainBox ul li")
        paginate = response.css(".wp-pagenavi a.page.larger")

        for episode in episodes:
            name = episode.css('a ::text').extract_first()
            url = episode.css('a ::attr(href)').extract_first()
            thumb = episode.css('.videoThumb a img ::attr(src)').extract_first()

            yield Request(url, callback=self.parse_episode, dont_filter=True, meta={ 'name': name, 'thumb': thumb } )
        
        if paginate:
            # name_page = paginate.css('a ::text').extract_first()
            url_page = paginate.css('a ::attr(href)').extract_first()


            yield Request(url_page, callback=self.parse_episodes, dont_filter=True )