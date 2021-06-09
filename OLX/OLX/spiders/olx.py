import scrapy


class OlxSpider(scrapy.Spider):
    name = 'olx'
    start_urls = ['https://olx.com.br/']
    lista_categorias = ['Apartamentos', 'Casas']

    def parse(self, response):
        tipo = response.xpath(
            '//*[@id="gatsby-focus-wrapper"]/div[3]/div[1]/div[2]/div[2]/div/div/ul/li')

        for i in tipo:
            nome_tipo = i.xpath("./a/small/text()").get()
            href = i.xpath("./a/@href").get()

            yield scrapy.Request(
                url=href,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        anuncios = response.xpath('//*[@id="ad-list"]/li')

        for j in anuncios:
            href = j.xpath('./a/@href').get()
            yield scrapy.Request(
                url=href,
                callback=self.parse_final
            )

    def parse_final(self, response):
        categoria = response.xpath(
            '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div[1]/div/a/text()').get()
