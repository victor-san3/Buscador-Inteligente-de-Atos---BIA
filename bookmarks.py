from typing import Dict, Union, List
from pypdf import PdfReader

def first_level_bookmark_dict(
    bookmark_list, reader: PdfReader, use_labels: bool = False,
) -> Dict[Union[str, int], List[str]]:
    """
    Extrai apenas os marcadores de primeiro nível como um dicionário plano.

    Args:
        bookmark_list: A lista de marcadores (reader.outline)
        use_labels: Se verdadeiro, usa rótulos de página. Se falso, usa índices de página.

    Retorna:
        Um dicionário que mapeia rótulos de página (ou índices de página) para uma lista de títulos de marcadores.
    """
    result = {}
    for item in bookmark_list:
        if isinstance(item, list):
            # Ignora marcadores aninhados (sub-marcadores)
            continue
        else:
            # Obtém o índice da página para o marcador atual
            page_index = reader.get_destination_page_number(item)
            # Obtém o rótulo da página correspondente ao índice
            page_label = reader.page_labels[page_index]
            # Define a chave como rótulo ou índice da página, dependendo do valor de use_labels
            key = page_label if use_labels else page_index
            
            # Inicializa a lista se a chave ainda não existir no dicionário
            if key not in result:
                result[key] = []
            
            # Adiciona o título do marcador à lista associada à chave
            result[key].append(item.title)
    
    return result

def second_level_bookmark_dict(
    bookmark_list, reader: PdfReader, use_labels: bool = False,
) -> Dict[Union[str, int], List[str]]:
    """
    Extrai apenas os marcadores de segundo nível como um dicionário plano.

    Args:
        bookmark_list: A lista de marcadores (reader.outline)
        use_labels: Se verdadeiro, usa rótulos de página. Se falso, usa índices de página.

    Retorna:
        Um dicionário que mapeia rótulos de página (ou índices de página) para uma lista de títulos de marcadores.
    """
    result = {}
    for item in bookmark_list:
        if isinstance(item, list):
            # Processa os sub-marcadores (segundo nível)
            for sub_item in item:
                if isinstance(sub_item, list):
                    # Ignora sub-marcadores de níveis mais profundos
                    continue
                else:
                    # Obtém o índice da página para o sub-marcador atual
                    page_index = reader.get_destination_page_number(sub_item)
                    # Obtém o rótulo da página correspondente ao índice
                    page_label = reader.page_labels[page_index]
                    # Define a chave como rótulo ou índice da página, dependendo do valor de use_labels
                    key = page_label if use_labels else page_index
                    
                    # Inicializa a lista se a chave ainda não existir no dicionário
                    if key not in result:
                        result[key] = []
                    
                    # Adiciona o título do sub-marcador à lista associada à chave
                    result[key].append(sub_item.title)
    
    return result

if __name__ == "__main__":
    # Lê o arquivo PDF usando o PdfReader
    reader = PdfReader("diarios/2024/08/20240827-doe-tce.pdf")
    
    # Extrai os marcadores de primeiro nível
    first_level_bms = first_level_bookmark_dict(reader.outline, reader, use_labels=True)
    
    # Extrai os marcadores de segundo nível
    second_level_bms = second_level_bookmark_dict(reader.outline, reader, use_labels=True)

    # Imprime os marcadores de primeiro nível
    print("Marcadores de Primeiro Nível:")
    for page_nb, titles in sorted(first_level_bms.items(), key=lambda n: f"{str(n[0]):>5}"):
        for title in titles:
            print(f"{page_nb:>3}: {title}")
    
    print("\nMarcadores de Segundo Nível:")
    # Imprime os marcadores de segundo nível
    for page_nb, titles in sorted(second_level_bms.items(), key=lambda n: f"{str(n[0]):>5}"):
        for title in titles:
            print(f"{page_nb:>3}: {title}")
