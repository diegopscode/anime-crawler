# -*- coding: utf-8 -*-
import scrapy

from scrapy import Request

class SearchTelescineSpider(scrapy.Spider):
    name = 'search-telescine'
    allowed_domains = ['https://www.animestelecine.net']
    start_urls = ['https://www.animestelecine.net/?s=Nanatsu+no+Taizai']

    def parse(self, response):
        animes = response.css(".anime-series .container-anime-serie a")

        for anime in animes:
            url = anime.css('::attr(href)').extract_first()

            yield Request(url, callback=self.parse_animes, dont_filter=True)

        # yield { 'url': url }

    def parse_animes(self, response):
        episodes = response.css(".elements-box .container-download-epi")

        url = episodes[0].css('a ::attr(href)').extract_first()
        yield Request(url, callback=self.parse_episode, dont_filter=True, meta={ 'name': 'teste' } )

        # for episode in episodes:
        #     name = episode.css('.titulo-down-epi h2 ::text').extract_first()
        #     url = episode.css('a ::attr(href)').extract_first()

        #     yield Request(url, callback=self.parse_episode, dont_filter=True, meta={ 'name': name } )

            # yield { 'name': name, 'url':url }

    def parse_episode(self, response):
        name = response.meta.get('name')
        video = response.css(".video-online-container video ::attr(src)").extract_first()
        test = response.css(".online-container").extract_first()

        yield { 'name': name, 'video': video, 'test': test }