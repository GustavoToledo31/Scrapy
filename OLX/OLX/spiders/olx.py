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

        categoria, condicao, condominio, iptu, area, quartos, banheiros, cep, municipio, bairro, logradouro = [
            np.NaN] * 11

        for detail in response.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div'):

            detalhe = detail.xpath('./div/dt/text()')

            if detalhe.get() == 'Categoria':
                try:
                    categoria = detail.xpath('./div/a/text()').get()
                    print("A Categoria foi:", categoria)
                except:
                    categoria = detail.xpath('./div/dd/text()').get()
            elif detalhe.get() == 'Tipo':
                try:
                    condicao = detail.xpath('./div/a/text()').get()
                except:
                    condicao = detail.xpath('./div/dd/text()').get()

            elif detalhe.get() == 'Condomínio':
                condominio = detail.xpath('./div/dd/text()').get()

            elif detalhe.get() == 'IPTU':
                iptu = detail.xpath('./div/dd/text()').get()

            elif detalhe.get() in ['Área construída', 'Tamanho', 'Área útil']:
                area = detail.xpath('./div/dd/text()').get()

            elif detalhe.get() == 'Quartos':
                quartos = detail.xpath('./div/a/text()').get()

            elif detalhe.get() == 'Banheiros':
                try:
                    banheiros = detail.xpath('./div/dd/text()').get()
                except:
                    banheiros = detail.xpath('./div/a/text()').get()

        for localizacao in response.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div[25]/div/div/div/div[1]/div[2]/div'):

            localiza = localizacao.xpath('./div/dt/text()')

            print("O VALOR DO LOCALIZA É:", localiza.get())

            if localiza.get() == 'CEP':
                cep = localizacao.xpath('./div/dd/text()').get()
                print("ESSE FOI O CEP EXTRAIDO:", cep)

            elif localiza.get() == 'Município':
                municipio = localizacao.xpath('./div/dd/text()').get()
                print("ESSE FOI O MUNICIPIO EXTRAIDO:", municipio)

            elif localiza.get() == 'Bairro':
                bairro = localizacao.xpath('./div/dd/text()').get()
                print("ESSE FOI O bairro EXTRAIDO:", bairro)

            elif localiza.get() == 'Logradouro':
                logradouro = localizacao.xpath('./div/dd/text()').get()
                print("ESSE FOI O logradouro EXTRAIDO:", logradouro)

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
            "Quantidade_Banheiros": banheiros,
            "CEP": cep,
            "Municipio": municipio,
            "Bairro": bairro,
            "Logradouro": logradouro
        }
