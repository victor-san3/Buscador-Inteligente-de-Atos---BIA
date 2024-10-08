import scrapy

class PareceresSpider(scrapy.Spider):
    name = 'pareceres_spider'
    start_urls = ['https://do.tce.sp.gov.br/sei/modulos/tcesp/boletim/md_boletim_tabloide.php?acao=selecionar_data']

    def parse(self, response):
        # Localiza a seção "PARECERES"
        secao_pareceres = response.xpath('//h1[@id="PARECERES"]')

        # Começa a partir do primeiro irmão do h1 "PARECERES"
        irmaos = secao_pareceres.xpath('following-sibling::*')

        # Inicializa um dicionário para armazenar os dados estruturados
        dados_secao = {'disponibilização': '', 'publicação': '', 'secao': 'PARECERES', 'subsecoes': {}}

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
                    # Remove caracteres \r\n e espaços em branco no início e fim de cada item
                    texto_conteudo_limpo = [item.strip().replace('\r\n', '') for item in texto_conteudo if item.strip()]
                    # Adiciona o conteúdo limpo ao subtítulo atual
                    dados_secao['subsecoes'][h2_atual].append({'conteudo': texto_conteudo_limpo})

        # Retorna todos os dados estruturados
        yield dados_secao
