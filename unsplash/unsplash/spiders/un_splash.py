import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import UnsplashItem
from itemloaders.processors import MapCompose
from urllib.parse import urljoin


class UnSplashSpider(CrawlSpider):
    name = "un_splash"
    allowed_domains = ["www.unsplash.com"]
    start_urls = ["https://www.unsplash.com"]

    rules = (Rule(LinkExtractor(restrict_xpaths=('//div[@class="pRk2s"]/ul/li/a')), callback="parse_item", follow=True),)

    def parse_item(self, response):
        # item = {}
        print(response.url)
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        # return item
        loader = ItemLoader(item=UnsplashItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        loader.add_xpath('name', '//figure[@itemprop="image"]/div/div/a/div/div[@class="MorZF"]/img/text()')
        
        relative_image_urls = response.xpath('//figure[@itemprop="image"]/div/div/a/div/div[@class="MorZF"]/img/@srcset').getall()

        absolute_image_urls = [urljoin("https://www.unsplash.com", img_url) for img_url in relative_image_urls]
        loader.add_value('image_urls', absolute_image_urls)

        yield loader.load_item()
