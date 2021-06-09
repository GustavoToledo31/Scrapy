import scrapy


class PalmeirasSpider(scrapy.Spider):
    name = 'Palmeiras'
    start_urls = [
        'https://pt.wikipedia.org/wiki/Sociedade_Esportiva_Palmeiras']

    def parse(self, response):
        for i in response.xpath('//*[@id="mw-content-text"]/div[1]/table[6]/tbody/tr[@bgcolor="#f9f9f9"]'):
            var = 1
            if len(i.xpath('./td')) == 4:
                var += 1
                comp = i.xpath(f'./td[{var}]/b/a/text()').get()
                print(comp)
                var += 1
                tit = i.xpath(f'./td[{var}]/b/text()').get()
                print(tit)
                var += 1
                temp = i.xpath(f'./td[{var}]/b/a/text()').getall()
                print(temp)

            elif len(i.xpath('./td')) == 3:
                comp = i.xpath(f'./td[{var}]/b/a/text()').get()
                print(comp)
                var += 1
                tit = i.xpath(f'./td[{var}]/b/text()').get()
                print(tit)
                var += 1
                temp = i.xpath(f'./td[{var}]/b/a/text()').getall()
                print(temp)

            yield {
                'Competição': comp,
                'Títulos': tit,
                'Temporadas': temp
            }
