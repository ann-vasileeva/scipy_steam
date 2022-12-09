import scrapy
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urljoin
import re
import json
from steam.items import SteamItem

queries = ['action', 'detective', 'history']


class SteamSpider(scrapy.Spider):
    name = 'SteamSpider'

    def start_requests(self):
        for query in queries:
            for i in range(1, 3):
                url = 'https://store.steampowered.com/search/?' + urlencode({'term': query, 'page': str(i)})
                yield scrapy.Request(url=url, callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        for res in response.xpath('//a[contains(@target, _target)]/@href').extract():
            yield scrapy.Request(url=res, callback=self.parse_product_page)

    def parse_product_page(self, response):

        item = SteamItem()

        name = response.css("#appHubAppName::text").get()
        category = response.xpath('//div[@class="blockbg"]/a[@href]/text()').extract()[1:]
        reviews_cnt = response.xpath('//div[@class="user_reviews_summary_bar"]//span/text()').extract()[1]
        overview = response.xpath('//div[@class="user_reviews_summary_bar"]//span/text()').extract()[0]
        developer = response.xpath('//div[@id="developers_list"]//a/text()').extract()
        release_date = response.css("div.date::text").get()
        tags = response.xpath('//div[@class="glance_tags popular_tags"]//a/text()').extract()
        discount = response.xpath('//div[@class="discount_final_price"]/text()').extract()
        price = response.xpath('//div[@class="game_purchase_price price"]/text()').extract()
        available_platforms = response.xpath(
            '//div[contains(@class, "game_area_sys_req sysreq_content")]//@data-os').extract()

        item['name'] = ''.join(name).strip()
        item['category'] = '/'.join(category).strip()
        item['reviews_cnt'] = ''.join(reviews_cnt).strip()
        item['overview'] = ''.join(overview).strip()
        item["developer"] = ''.join(developer).strip()
        item['release_date'] = ''.join(release_date).strip()
        for tag in tags:
            tag = tag.strip()
        item['tags'] = ','.join(tags).strip()
        if discount:
            item['price'] = ''.join(discount).strip()
        else:
            item['price'] = ''.join(price).strip()
        item['available_platforms'] = ",".join(available_platforms).strip()

        yield item
