import scrapy

class SentencasSpider(scrapy.Spider):
    name = 'sentencas_spider'
    start_urls = ['https://do.tce.sp.gov.br/sei/modulos/tcesp/boletim/md_boletim_tabloide.php?acao=selecionar_data']

    def parse(self, response):
        # Localiza a seção "SENTENÇAS"
        secao_sentencas = response.xpath('//h1[@id="SENTENÇAS"]')

        # Começa a partir do primeiro irmão do h1 "SENTENÇAS"
        irmaos = secao_sentencas.xpath('following-sibling::*')

        # Inicializa um dicionário para armazenar os dados estruturados
        dados_secao = {'disponibilização': '', 'publicação': '', 'secao': 'SENTENÇAS', 'subsecoes': {}}

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

                            # Extrai outro conteúdo após processar tabelas e adiciona ao mesmo item
                            outro_conteudo = conteudo.xpath('.//text()[not(ancestor::table)]').getall()
                            conteudo_limpo = ' '.join([texto.strip() for texto in outro_conteudo if texto.strip()])
                            if conteudo_limpo:
                                if isinstance(dados_secao['subsecoes'][h2_atual][-1]['conteudo'], dict):
                                    dados_secao['subsecoes'][h2_atual][-1]['conteudo']['EXTRATO'] = conteudo_limpo
                                else:
                                    dados_secao['subsecoes'][h2_atual][-1]['conteudo'] += ' ' + conteudo_limpo
                    else:
                        # Extrai outro conteúdo se nenhuma tabela for encontrada
                        outro_conteudo = conteudo.xpath('.//text()').getall()
                        conteudo_limpo = ' '.join([texto.strip() for texto in outro_conteudo if texto.strip()])
                        if conteudo_limpo:
                            dados_secao['subsecoes'][h2_atual].append({'conteudo': conteudo_limpo})

        # Retorna todos os dados estruturados
        yield dados_secao
