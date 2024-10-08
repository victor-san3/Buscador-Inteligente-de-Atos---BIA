import scrapy

class ComunicadosSpider(scrapy.Spider):
    name = 'comunicados_spider'
    start_urls = ['https://do.tce.sp.gov.br/sei/modulos/tcesp/boletim/md_boletim_tabloide.php?acao=selecionar_data']

    def parse(self, response):
        # Localiza a seção "COMUNICADOS"
        secao_comunicados = response.xpath('//h1[@id="COMUNICADOS"]')

        # Começa a partir do primeiro irmão do h1 "COMUNICADOS"
        irmaos = secao_comunicados.xpath('following-sibling::*')

        # Inicializa um dicionário para armazenar os dados estruturados
        dados_secao = {'disponibilização': '', 'publicação': '', 'secao': 'COMUNICADOS', 'subsecoes': {}}

        # Extrai a data de disponibilização e a data de publicação
        dados_secao['disponibilização'] = response.xpath('//*[@id="disponibilizacao-publicacao"]/text()[1]').get()[-10:]
        dados_secao['publicação'] = response.xpath('//*[@id="disponibilizacao-publicacao"]/text()[2]').get()[-10:]

        h2_atual = None
        for irmao in irmaos:
            # Interrompe o loop se outro h1 for encontrado
            if irmao.root.tag == 'h1':
                break

            # Processa elementos h2
            if irmao.root.tag == 'h2':
                h2_atual = irmao.xpath('text()').get()
                # Inicializa uma lista para o subtítulo atual se ainda não estiver presente
                if h2_atual not in dados_secao['subsecoes']:
                    dados_secao['subsecoes'][h2_atual] = []

            # Processa elementos div com classe "publicacao"
            elif irmao.root.tag == 'div' and irmao.xpath('@class').get() == 'publicacao':
                # Extrai dados das divs "conteudo" dentro da div "publicacao"
                divs_conteudo = irmao.xpath('.//div[@class="conteudo"]')

                for conteudo in divs_conteudo:
                    # Extrai o texto ou qualquer dado específico necessário da div "conteudo"
                    texto_conteudo = conteudo.xpath('.//text()').getall()
                    # Adiciona o conteúdo ao subtítulo atual
                    dados_secao['subsecoes'][h2_atual].append({'conteudo': texto_conteudo})

        # Retorna todos os dados estruturados
        yield dados_secao
