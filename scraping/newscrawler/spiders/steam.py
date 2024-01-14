import scrapy
from scrapy import Request
from ..items import ArticleItem

# #id .class

class MySpider(scrapy.Spider):
    name = "steam"
    allowed_domains = ["https://store.steampowered.com/search/"]
    start_urls = ['https://store.steampowered.com/search/']
    custom_settings = {
            "HTTPCACHE_ENABLED":True,
            "CONCURRENT_REQUESTS_PER_DOMAIN":100
        }

    def parse(self, response):

        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css("#search_resultsRows").css(".responsive_search_name_combined").css(".title").css("span::text").extract(),
            response.css("#search_resultsRows").css("a::attr(href)").extract())
        }


        yield ArticleItem(
            name=response.url,
        )

        for name, link in all_links.items():
            yield ArticleItem(
                name=name,
            )
            #self.log(f'Nom: {name}, Lien: {link}')

        for link in all_links.values():
            yield Request(link, callback=self.parse_category)

    def parse_category(self, response):
        for article in response:
            name = response.css(".apphub_AppName").css("div::text").extract_first()
            yield ArticleItem(
                name=name,
            )

    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())
