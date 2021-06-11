import scrapy
from functools import partial
import numpy as np


class OlxSpider(scrapy.Spider):
    name = 'olx'
    start_urls = ['https://olx.com.br/']

    def parse(self, response):
        tipo = response.xpath(
            '// *[@id="gatsby-focus-wrapper"]/div[3]/div[1]/div[2]/div[2]/div/div/ul/li[1]')

        nome_tipo = tipo.xpath("./a/small/text()").get()
        href = tipo.xpath("./a/@href").get()

        yield scrapy.Request(
            url=href,
            callback=partial(self.parse_detail, nome_tipo)
        )

    def parse_detail(self, nome_tipo_1, response):
        print(response)
        for i in [1, 2, 5, 6, 7, 9] + list(range(10, 26)) + list(range(27, 37)) + list(range(38, 56)):
            anuncio = response.xpath(f'//*[@id="ad-list"]/li[{i}]')
            href = anuncio.xpath('./a/@href').get()

            yield scrapy.Request(
                url=href,
                callback=partial(self.parse_final_imoveis, nome_tipo_1)
            )

    def parse_final_imoveis(self, nome_tipo_2, response):
        nome_anuncio = response.xpath(
            '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[14]/div/div/h1/text()').get()

        preco = response.xpath(
            '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[12]/div/div/div/div/div[1]/div/h2/text()').get()

        categoria, condicao, condominio, iptu, area, quartos, banheiros = [
            np.NaN] * 7

        for detail in response.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div'):

            print("O VALOR DO DETAIL É:", detail.xpath('./div/dt/text()').get())

            detalhe = detail.xpath('./div/dt/text()').get()

            if detalhe == 'Categoria':
                categoria = response.xpath(
                    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div[1]/div/a/text()').get()

            elif detalhe == 'Tipo':
                print("ENTREI NO TIPO")
                try:
                    condicao = response.xpath(
                        '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div[2]/div/a/text()').get()
                except:
                    condicao = response.xpath(
                        '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div[2]/div/dd/text()').get()

            elif detalhe == 'Condomínio':
                print("ENTREI EM CONDOMINIO")
                condominio = response.xpath(
                    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div[3]/div/dd/text()').get()

            elif detalhe == 'IPTU':
                print("ENTREI NO IPTU")
                iptu = response.xpath(
                    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div[4]/div/dd/text()').get()

                print("O VALOR DO IPTU É:", iptu)

            elif detalhe in ['Área construída', 'Tamanho']:
                print("ENTREI NO TAMANHO")
                area = response.xpath(
                    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div[5]/div/dd/text()').get()

            elif detalhe == 'Quartos':
                quartos = response.xpath(
                    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div[6]/div/a/text()').get()

            elif detalhe == 'Banheiros':
                banheiros = response.xpath(
                    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div[7]/div/dd/text()').get()

        yield {
            "Tipo_do_Produto": nome_tipo_2,
            "Descricao": nome_anuncio,
            "Preco": preco,
            "Categoria": categoria,
            "Condicao": condicao,
            "Preco_Condominio": condominio,
            "IPTU": iptu,
            "Area": area,
            "Quantidade_Quartos": quartos,
            "Quantidade_Banheiros": banheiros
        }
