# -*- coding: utf-8 -*-
import scrapy

from scrapy import Request

class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['http://www.animesorion.tv']
    start_urls = ['http://www.animesorion.tv/?s=Angel+Beats&cat=780&BUSCAR=BUSCAR']

    # def start_requests(self):
    #     start = self.start_urls[0] + "/search=dragon+ball+super"
    #     yield Request(start, callback=self.parse, dont_filter=True)

    def parse(self, response):
        anime = response.css(".contentBox ul li a")

        # title = anime.css('::text').extract_first()
        url = anime.css('::attr(href)').extract_first()

        yield Request(url, callback=self.parse_animes, dont_filter=True)

        # yield { 'url': url }

    def parse_animes(self, response):
        episodes = response.css(".lcp_catlist li a")

        # yield { 'episodes': episodes }

        for episode in episodes:
            name = episode.css('::text').extract_first()
            url = episode.css('::attr(href)').extract_first()

            yield Request(url, callback=self.parse_episode, dont_filter=True, meta={ 'name': name } )

            # yield { 'name': name, 'url':url }

    def parse_episode(self, response):
        name = response.meta.get('name')
        video = response.css(".contentBox video source ::attr(src)").extract_first()

        yield { 'name': name, 'video': video }