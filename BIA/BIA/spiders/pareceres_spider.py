import scrapy

class SentencasSpider(scrapy.Spider):
    name = 'sentencas_spider'
    start_urls = ['https://do.tce.sp.gov.br/sei/modulos/tcesp/boletim/md_boletim_tabloide.php?acao=selecionar_data']

    def parse(self, response):
        # Locate the "SENTENÇAS" section
        sentencas_section = response.xpath('//h1[@id="SENTENÇAS"]')

        # Start from the first sibling of the "SENTENÇAS" h1
        siblings = sentencas_section.xpath('following-sibling::*')

        # Initialize a dictionary to hold the structured data
        section_data = {'section': 'SENTENÇAS', 'subtitles': {}}

        current_h2 = None
        for sibling in siblings:
            # Break the loop if another h1 is encountered
            if sibling.root.tag == 'h1':
                break

            # Process h2 elements
            if sibling.root.tag == 'h2':
                current_h2 = sibling.xpath('text()').get()
                # Initialize a list for the current subtitle if not already present
                if current_h2 not in section_data['subtitles']:
                    section_data['subtitles'][current_h2] = []

            # Process div elements with class "publicacao"
            elif sibling.root.tag == 'div' and sibling.xpath('@class').get() == 'publicacao':
                # Extract data from "conteudo" divs within the "publicacao" div
                conteudo_divs = sibling.xpath('.//div[@class="conteudo"]')

                for conteudo in conteudo_divs:
                    # Extract the text or any specific data you need from the "conteudo" div
                    conteudo_text = conteudo.xpath('.//text()').getall()
                    # Append the content to the current subtitle
                    section_data['subtitles'][current_h2].append(conteudo_text)

        # Yield the entire structured data
        yield section_data
