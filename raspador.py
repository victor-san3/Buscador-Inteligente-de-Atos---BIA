import os
import tika
from tika import parser as p 
import requests

def download_pdf(ano, mes, dia):
    # URL base
    base_url = "https://doe.tce.sp.gov.br/pdf"

    # Formata a URL
    url = f"{base_url}/{ano}/{mes}/doe-tce-{ano}-{mes}-{dia}.pdf"

    # Faz o request
    response = requests.get(url)
    
    # Verifica se o request foi bem sucedido
    if response.status_code == 200:
        # Garante que o diretório existe no sistema
        diretorio = f"diarios/{ano}/{mes}"
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        
        # Caminho para o diretório de salvamento
        pdf_path = f"{diretorio}/{ano}{mes}{dia}-doe-tce.pdf"
        
        # Grava o pdf
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        print(f"Arquivo salvo em {pdf_path}")

        # Chama a função de tratamento do pdf para txt
        txt_path = f"{diretorio}/{ano}{mes}{dia}-doe-tce.txt"

        parse_pdf(pdf_path, txt_path)
    else:
        print(f"Falha ao obter o diário de {dia}/{mes}/{ano}. Status: {response.status_code}")

def parse_pdf(file_path, output_path):
    parsed_pdf = p.from_file(file_path)

    resultado = parsed_pdf["content"].strip()

    resultado_limpo = resultado.replace('-\n', '')

    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(resultado_limpo)


if __name__ == "__main__":
    ano = "2024"
    mes = input("Mês (mm): ").strip()
    dia = input("Dia (dd): ").strip()

    download_pdf(ano, mes, dia)
