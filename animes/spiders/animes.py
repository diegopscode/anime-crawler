# -*- coding: utf-8 -*-
import scrapy


class AnimesSpider(scrapy.Spider):
    name = 'animes'
    allowed_domains = ['http://www.animesonlinebr.com.br']
    start_urls = ['http://www.animesonlinebr.com.br/video/5604250']

    def parse(self, response):
        for video_url in response.css("#player video ::attr(src)").extract():
            yield {'video_url': video_url}

        for title in response.css(".contentBox > h1.single ::text").extract():
            yield {'title': title}