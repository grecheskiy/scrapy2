import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class WikimediaSpider(CrawlSpider):
    name = "wikimedia"
    allowed_domains = ["commons.wikimedia.org"]
    start_urls = ["https://commons.wikimedia.org/wiki/Category:Featured_pictures_on_Wikimedia_Commons"]

    rules = (Rule(LinkExtractor(restrict_xpaths=('//div[@id="mw-category-media"]/ul/li/div[@class="gallerytext"]/a')), callback="parse_image_page", follow=True),
    )

    def parse_image_page(self, response):
        full_image_url = response.xpath('//div[@class="fullImageLink"]/a/@href')
        if full_image_url:
            yield scrapy.Request(response.urljoin(full_image_url), callback=self.save_image)


    def save_image(self, response):
        filename = response.url.split('/')[-1]
        with open(f'images/{filename}', 'wb') as f:
            f.write(response.body)