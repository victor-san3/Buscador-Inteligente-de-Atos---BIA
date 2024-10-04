import scrapy

class AcordoesSpider(scrapy.Spider):
    name = 'acordaos_spider'
    start_urls = ['https://do.tce.sp.gov.br/sei/modulos/tcesp/boletim/md_boletim_tabloide.php?acao=selecionar_data']

    def parse(self, response):
        # Localiza a seção "ACÓRDÃOS"
        secao_acordaos = response.xpath('//h1[@id="ACÓRDÃOS"]')

        # Começa a partir do primeiro irmão do h1 "ACÓRDÃOS"
        irmaos = secao_acordaos.xpath('following-sibling::*')

        # Inicializa um dicionário para armazenar os dados estruturados
        dados_secao = {'secao': 'ACÓRDÃOS', 'subsecoes': {}}

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
                    # Tenta extrair tabelas com id "pia_processo"
                    tabelas = conteudo.xpath('.//table[@id="pia_processo"]')
                    if tabelas:
                        for tabela in tabelas:
                            dados_tabela = {}
                            linhas = tabela.xpath('.//tr')
                            for linha in linhas:
                                # Extrai texto de <th> e <td>
                                chave = linha.xpath('.//th//text()').get()
                                valor = linha.xpath('.//td//text()').getall()
                                # Limpa e combina o texto do valor
                                valor_limpo = ' '.join([v.strip() for v in valor if v.strip()])
                                if chave and valor_limpo:
                                    dados_tabela[chave.strip()] = valor_limpo
                            # Adiciona os dados estruturados da tabela ao subtítulo atual
                            dados_secao['subsecoes'][h2_atual].append({'conteudo': dados_tabela})
                    else:
                        # Extrai outro conteúdo se nenhuma tabela for encontrada
                        outro_conteudo = conteudo.xpath('.//text()').getall()
                        conteudo_limpo = ' '.join([texto.strip() for texto in outro_conteudo if texto.strip()])
                        if conteudo_limpo:
                            dados_secao['subsecoes'][h2_atual].append({'conteudo': conteudo_limpo})

        # Retorna todos os dados estruturados
        yield dados_secao
