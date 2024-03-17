import scrapy


class AsiaAreaSpider(scrapy.Spider):
    name = "asia_area"
    allowed_domains = ["theglobaleconomy.com"]
    start_urls = ["https://theglobaleconomy.com/rankings/forest_area/Asia/"]

    def parse(self, response):
        asia_area = response.xpath("//table/tbody/tr")
        for country in asia_area:
            name = country.xpath(".//td/a/text()").get().strip()
            link = country.xpath(".//td/a/@href").get()
            yield response.follow(url=link, callback=self.parse_asia, 
                                  meta={'country_name' : name})
            
    def parse_asia(self, response):
        rows = response.xpath('//table[@id="benchmarkTable"]/tbody/tr')
        for row in rows:
            related = row.xpath(".//td/a/text()").get()
            latest = row.xpath(".//td[2]/text()").get()
            reference = row.xpath(".//td[3]/text()").get().strip()
            measure = row.xpath(".//td[4]/text()").get()
            name = response.request.meta['country_name']
            yield {
                'country_name' : name,
                'Related_indicators' : related,
                'Latest_value' : latest,
                'Reference' : reference,
                'Measure' : measure
            }
