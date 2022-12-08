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
        category = response.css("div.blockbg") # Нужно ухх как почистить
        reviews_cnt = response.css("span.responsive_hidden::text")[1].get()
        overview = response.css("span.game_review_summary.positive::text").get()
        release_date = response.css("div.date::text").get()  #19 Apr, 2019
        tags = response.css("div.glance_tags.popular_tags")[0].get() ## каша, выудить нужное
        discount = response.css("div.discount_final_price::text").get()
        original_price = response.css("div.game_purchase_price.price::text").get()  #'\r\n\t\t\t\t\t\t\t435 pуб.\t\t\t\t\t\t'
        available_platforms = response.css("div.sysreq_tabs").get()
        '<div class="sysreq_tabs">\r\n\t\t\t\t\t\t\t\t\t<div class="sysreq_tab active" data-os="win">\r\n\t\t\t\t\t\tWindows\t\t\t\t\t</div>\r\n\t\t\t\t\t\t\t\t\t<div class="sysreq_tab " ' \
        'data-os="mac">\r\n\t\t\t\t\t\tmacOS\t\t\t\t\t</div>\r\n\t\t\t\t\t\t\t\t\t<div class="sysreq_tab " data-os="linux">\r\n\t\t\t\t\t\tSteamOS + Linux\t\t\t\t\t</div>\r\n\t\t\t\t\t\t\t\t<div style="clear: left;"></div>\r\n\t\t\t</di'

        item['name'] = name
        item['category'] = None
        item['reviews_cnt'] = response.css("span.responsive_hidden::text")[1].get()

        title = response.xpath('//h1/text()').extract()
        category = response.xpath('//ol[contains(@class, SnowBreadcrumbs_SnowBreadcrumbs__list__1xzrg)]/li/a/text()').extract()
        price = response.xpath('//div[contains(@class, snow-price_SnowPrice__secondPrice__18x8np)][1]/text()').extract()
        sale_price = response.xpath('//div[contains(@class, snow-price_SnowPrice__mainM__18x8np)][1]/text()').extract()
        delivery = response.xpath('//div[contains(@class, SnowProductDelivery_SnowProductDelivery__item__y5v67)[0]/span[1]/text()').extract()
        rating = response.xpath('//p[contains(@class, SnowReviews_ProductRating__ratingAverage__17pz0)[0]/text()').extract()
        item["title"] = ''.join(title).strip()
        item["category"] = '/'.join(category).strip()
        item["price"] = ''.join(price).strip()
        item["sale_price"] = ''.join(sale_price).strip()
        item["delivery"] = ''.join(delivery).strip()
        item["rating"] = ''.join(rating).strip()


        yield item