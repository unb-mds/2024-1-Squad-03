import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import zipfile
from tqdm import tqdm
from lxml import etree as ET
from time import sleep

# Fun��o para capturar o link do banco de dados do DOU
def captura_link_banco_de_dados_DOU_mes(ano, mes):
    url_bd_dou = "https://www.in.gov.br/acesso-a-informacao/dados-abertos/base-de-dados?"
    meses = ['NULL - (meses equivalentes aos seus n�meros)', 'Janeiro', 'Fevereiro', 'Mar�o', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    data_input = datetime(ano, mes, 1)
    data_atual = datetime.now()

    if data_input > data_atual:
        return "Data informada � posterior � data atual."
    else:
        url_consulta = url_bd_dou + "ano=" + str(ano) + "&mes=" + meses[mes]
        response = requests.get(url_consulta)

        # Verifica se a requisi��o foi bem sucedida
        if response.status_code == 200:
            html_content = response.content  # Pega o conte�do HTML da resposta
            # Usa o Beautiful Soup para parsear o HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Encontrar todos os elementos <a>
            links = soup.find_all('a')

            # Iterar sobre os links e encontrar o href que cont�m S03 e .zip
            for link in links:
                href = link.get('href')
                if href and 'S03' in href and '.zip' in href:
                    return href
            
            return "Nenhum link encontrado para esse periodo"
        else:
            return f"Falha ao acessar a p�gina. Status code: {response.status_code}"

def faz_download_do_zip(link_html, anor, mesr, max_retries=3):
    # Obt�m o diret�rio atual
    direct = os.getcwd()
    diretorio_content = os.path.join(direct, "content")

    if not os.path.exists(diretorio_content):
        os.makedirs(diretorio_content)
        
    # Verifica se os par�metros ano e mes est�o presentes na URL    
    salva = os.path.join(diretorio_content, f"{anor} - {mesr}")
    if not os.path.exists(salva):
        os.makedirs(salva)

    # Obt�m o nome do arquivo ZIP a partir do link
    nome_arquivo_zip = link_html.split('/')[-1]

    # L�gica de retry
    for attempt in range(max_retries):
        try:
            # Faz o download do arquivo ZIP com barra de progresso
            r = requests.get(link_html, stream=True)
            total_size = int(r.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            t = tqdm(total=total_size, unit='iB', unit_scale=True)
            with open(os.path.join(diretorio_content, nome_arquivo_zip), "wb") as f:
                for data in r.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
            t.close()
            break  # Se o download for bem-sucedido, sai do loop
        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError) as e:
            print(f"Erro no download: {e}. Tentativa {attempt + 1} de {max_retries}")
            t.close()
            sleep(5)  # Espera 5 segundos antes de tentar novamente
    else:
        raise Exception("Falha no download ap�s v�rias tentativas")

    # Extrai o arquivo ZIP para uma pasta com o ano e o m�s com barra de progresso
    with zipfile.ZipFile(os.path.join(diretorio_content, nome_arquivo_zip), 'r') as zip_ref:
        zip_size = sum((file.file_size for file in zip_ref.infolist()))
        t = tqdm(total=zip_size, unit='iB', unit_scale=True)
        for file in zip_ref.infolist():
            t.update(file.file_size)
            zip_ref.extract(file, salva)
        t.close()
    
    # Remove o arquivo ZIP ap�s a extra��o
    os.remove(os.path.join(diretorio_content, nome_arquivo_zip))
    
    # Apaga todos os arquivos que n�o terminem com .xml com barra de progresso
    for root, dirs, files in os.walk(salva):  # Alterado para garantir que apenas os arquivos na pasta de extra��o sejam verificados
        for file in tqdm(files, desc="Removendo arquivos que n�o s�o .xml"):
            if not file.endswith(".xml"):
                os.remove(os.path.join(root, file))
    
    # Retorna o diret�rio onde os arquivos foram extra�dos
    return salva
def processa_xml_obtem_brasilia(diretorio_dos_xml):
    # Lista de palavras espec�ficas
    palavras_especificas = ["Brasilia", "Bras�lia", " DF "]
    
    # Iterar sobre todos os arquivos no diret�rio
    for root, dirs, files in os.walk(diretorio_dos_xml):
        for file in tqdm(files, desc="Processando arquivos XML"):
            caminho_arquivo = os.path.join(root, file)
            if file.endswith(".xml"):
                try:
                    # Verifica o conte�do dos arquivos XML usando lxml
                    parser = ET.XMLParser(recover=True)
                    tree = ET.parse(caminho_arquivo, parser)
                    root_element = tree.getroot()
                    conteudo = ET.tostring(root_element, encoding='utf-8').decode('utf-8')

                    # Verifica se alguma das palavras espec�ficas est� no conte�do do XML
                    if sum(conteudo.count(palavra) for palavra in palavras_especificas) != len(palavras_especificas):
                        os.remove(caminho_arquivo)
                    else:
                        # Verifica se as palavras "horarios" ou "hor�rio" est�o pr�ximas das palavras-chave
                        for palavra_chave in palavras_especificas:
                            if palavra_chave in conteudo:
                                indice_palavra_chave = conteudo.index(palavra_chave)
                                trecho_analisado = conteudo[max(0, indice_palavra_chave - 30):indice_palavra_chave + len(palavra_chave) + 30]
                                if "horarios" in trecho_analisado or "hor�rio" in trecho_analisado:
                                    os.remove(caminho_arquivo)
                                    break  # Se encontrar, n�o precisa mais verificar o resto das palavras-chave
                except ET.XMLSyntaxError:
                    print(f"Arquivo XML malformado removido: {caminho_arquivo}")
                    os.remove(caminho_arquivo)

    print("Processamento de arquivos XML conclu�do!")
    return diretorio_dos_xml
def processa_xml_licitacoes(diretorio_dos_xml):
    # Lista de palavras relacionadas a licita��es
    palavras_licitacao = [" licita��o ", " licitacao ", " licitacoes "]
    
    # Iterar sobre todos os arquivos no diret�rio
    for root, dirs, files in os.walk(diretorio_dos_xml):
        for file in tqdm(files, desc="Processando arquivos XML para verificar licita��es"):
            caminho_arquivo = os.path.join(root, file)
            if file.endswith(".xml"):
                # Verifica o conte�do dos arquivos XML
                tree = ET.parse(caminho_arquivo)
                root_element = tree.getroot()
                conteudo = ET.tostring(root_element, encoding='utf-8').decode('utf-8')

                # Verifica se o vetor de palavras relacionadas a licita��es est� presente
                if not any(palavra_licitacao in conteudo for palavra_licitacao in palavras_licitacao):
                    os.remove(caminho_arquivo)

    print("Verifica��o de licita��es nos arquivos XML conclu�da!")  
# Exemplo de uso: