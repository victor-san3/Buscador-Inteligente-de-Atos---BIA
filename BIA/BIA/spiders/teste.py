import scrapy

"""
https://www.phind.com/search?cache=un1haovn9uvok2xgpr2vlsx2
"""

from scrapy.crawler import CrawlerProcess
from BIA.spiders.comunicados_spider import ComunicadosSpider

class ParentSpider(scrapy.Spider):
    name = 'parent_spider'
    start_urls = ['https://do.tce.sp.gov.br/sei/modulos/tcesp/boletim/md_boletim_tabloide.php?acao=selecionar_data']

    def parse(self, response):
        # Fetch all section names
        sections = response.xpath('//*[@id="secaoFiltro"]//a/text()').getall()

        # Start a CrawlerProcess to run child spiders
        process = CrawlerProcess()

        for section_name in sections:
            if section_name == 'COMUNICADOS':
                process.crawl(ComunicadosSpider, section_name=section_name)
            # Add more elif blocks for other sections

        process.start()  # Start the crawling process

