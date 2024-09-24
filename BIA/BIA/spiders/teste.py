import scrapy

"""
https://www.phind.com/search?cache=un1haovn9uvok2xgpr2vlsx2
"""


class TesteSpider(scrapy.Spider):
    name = "teste"
    allowed_domains = ["do.tce.sp.gov.br"]
    start_urls = ["https://do.tce.sp.gov.br/sei/modulos/tcesp/boletim/md_boletim_tabloide.php?acao=selecionar_data"]

    def parse(self, response):
        # Fetch all section names
        sections = response.xpath('//*[@id="secaoFiltro"]//a/text()').getall()

        # Iterate over each section
        for section_name in sections:
            # Construct dynamic XPath for each section
            section_title_xpath = f'//*[@id="{section_name}"]/text()'
            section_subtitle_xpath = f'//*[@id="container"]/h2[following-sibling::h1[@id="{section_name}"]]/text()'
            section_data_xpath = f'//*[@id="container"]/div[preceding-sibling::h1[@id="{section_name}"]]/div/text()'

            # Extract data for each section
            section_title = response.xpath(section_title_xpath).get()
            section_subtitle = response.xpath(section_subtitle_xpath).get()
            section_data = response.xpath(section_data_xpath).getall()

            # Yield the extracted data
            yield {
                'section': section_name,
                'title': section_title,
                'subtitle': section_subtitle,
                'data': section_data
            }
