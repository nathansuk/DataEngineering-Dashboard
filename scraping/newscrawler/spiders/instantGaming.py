import scrapy
from scrapy import Request
from ..items import UrlStock
from ..items import Lien


def get_list_url():
    """
    :return: La liste des URL récupérées à partir du nombre de page
    """
    start_url = []
    for i in range(1, 218+1):
        start_url.append('https://www.instant-gaming.com/fr/rechercher/?page=' + str(i))

    return start_url

# Instantiation du spider
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
            title = str(item.css('.game-title::text').extract_first())  # Titre du jeu
            developers = item.xpath('//a[@content="Developers"]/text()').get()  # Développeur
            publisher = item.xpath('//a[@content="Publishers"]/text()').get()  # Editeur
            ig_review_average = str(item.css(".show-more-reviews").css(".high").css("div::text").extract_first())  # Note moyenne
            ig_review_number = str(item.css('div.based span.link::text').extract_first())  # Nombre de review (note)
            discounted = str(item.css('.discounted::text').extract_first())  # Montant de la réduction (valeur absolue en %)
            date_published = str(item.css('.release-date::text').extract_first())  # Date de sortie
            final_price = str(item.css('.total::text').extract_first())  # Date de sortie
            tags = str(item.css('a.searchtag::text').getall()) # Liste des "tags" (sous-catégories)
            genres = str(item.css('div.genres a.tag::text').getall()) # Type de jeu (catégorie)
            original_selling_platform = str(item.css('div.subinfos a.platform').get()) # Plateforme de vente à l'origine
            playable_platform = item.css('select#platforms-choices option::attr(value)').getall() or ['PC'] # Jouable sur quelle plateforme
            # Liste des éditions disponibles (Standard, Collector, Heroic etc..)
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
                tags = tags.replace('\\n', ''),
                genres = genres.replace('\u00e9', 'é'),
                original_selling_platform = original_selling_platform,
                playable_platform = playable_platform,
                editions = editions
            )
