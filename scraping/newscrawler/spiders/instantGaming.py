import scrapy
from scrapy import Request
from ..items import UrlStock
from ..items import Lien

# #id .class
# response.css(".pagination").css("li")[-2].css("a::text").extract()


def get_list_url():
    start_url = []
    for i in range(1, 218+1):
        start_url.append('https://www.instant-gaming.com/fr/rechercher/?page=' + str(i))

    return start_url

class MySpider(scrapy.Spider):
    name = "instantGaming"
    allowed_domains = ["www.instant-gaming.com"]
    start_urls = get_list_url()
    comptage = []

    def parse(self, response):

        """
        tendances = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".search").css(".listing-items").css(".item").css(".force-badge").css(".information").css("span.title::text").extract(),
            response.css(".listing-items").css(".item").css(".force-badge").css(".cover").css("a::attr(href)").extract())
        }
        """

        list_lien = response.css('a.cover::attr(href)').extract()
        for lien in list_lien:
            yield Lien (
                url = lien
            )

        for link in list_lien:
            yield Request(link, callback=self.parse_url)

    def parse_url(self, response):
        for item in response.css(".product-container"):
            title = str(item.css('.game-title::text').extract_first())
            developers = item.xpath('//a[@content="Developers"]/text()').get()
            publisher = item.xpath('//a[@content="Publishers"]/text()').get()
            ig_review_average = str(item.css(".show-more-reviews").css(".high").css("div::text").extract_first())
            ig_review_number = str(item.css('div.based span.link::text').extract_first())
            discounted = str(item.css('.discounted::text').extract_first())
            date_published = str(item.css('.release-date::text').extract_first())
            final_price = str(item.css('.total::text').extract_first())
            tags = item.css('a.searchtag::text').getall()
            genres = str(item.css('div.genres a.tag::text').getall())
            original_selling_platform = str(item.css('div.subinfos a.platform').get())
            playable_platform = item.css('select#platforms-choices option::attr(value)').getall() or ['PC']
            editions = { str(option.css('::text').get().strip().replace('\u20ac', '')): str(option.css('::attr(data-product-price)').get()).replace('\u20ac', '') for option in item.css('select#editions-choices option') }

            if len(original_selling_platform.split('\n')) > 4 :
                original_selling_platform = list(original_selling_platform.split('\n'))[4]
            else :
                original_selling_platform = original_selling_platform


            yield UrlStock(
                title = title.replace('\u2019', '\''),
                developers = developers,
                publisher = publisher,
                ig_review_average = ig_review_average.replace('\n', ''),
                ig_review_number = ig_review_number.replace(' tests', ''),
                discounted = discounted.replace('-', '').replace('%', ''),
                date_published = date_published.replace('\n', ''),
                final_price = final_price.replace('€', ''),
                tags = tags,
                genres = genres.replace('\u00e9', 'é'),
                original_selling_platform = original_selling_platform,
                playable_platform = playable_platform,
                editions = editions
            )
