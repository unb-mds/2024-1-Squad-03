import requests
import json
import time
from datetime import date, timedelta

def buscar_dados_licitacoes(nome_arquivo_codigos_orgaos, nome_arquivo_saida):
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/licitacoes"
    headers = {"chave-api-dados": "707da7564df67f01820e5cf1bc4ce3f4"}
    data_final = date.today().strftime("%d/%m/%Y")
    data_inicio = (date.today() - timedelta(days=25)).strftime("%d/%m/%Y")

    with open(nome_arquivo_codigos_orgaos, 'r', encoding='utf-8') as f:
        codigos_orgaos = json.load(f)

    dados_totais = []
    licitacoes_df = []

    for codigo_orgao in codigos_orgaos:
        # params = {
        #     "dataInicial": data_inicio,
        #     "dataFinal": data_final,
        #     "codigoOrgao": codigo_orgao,
        #     "pagina": "1"
        # }

        params = {
            "dataInicial": "01/01/2024",
            "dataFinal": "01/02/2024",
            "codigoOrgao": codigo_orgao,
            "pagina": "1"
        }
        
        paginas_vazias = 0 
        
        while paginas_vazias < 1:
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()

                data_json = response.json()

                if not data_json:
                    paginas_vazias += 1
                    print(f"Página {params['pagina']} vazia para o órgão {codigo_orgao}.")
                else:
                    paginas_vazias = 0
                    dados_totais.extend(data_json)
                    print(f"Dados do órgão {codigo_orgao}, página {params['pagina']} adicionados.")

                    for licitacao in data_json:
                        if licitacao['municipio']['uf']['nome'] == "DF":
                            licitacoes_df.append(licitacao)

                params['pagina'] = str(int(params['pagina']) + 1)
            except requests.exceptions.RequestException as e:
                print(f"Erro ao fazer a requisição para o órgão {codigo_orgao}, página {params['pagina']}: {e}")

    with open('dados_licitacoes_totais_df.json', 'w', encoding='utf-8') as f:
        json.dump(licitacoes_df, f, ensure_ascii=False, indent=4)
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(dados_totais, f, ensure_ascii=False, indent=4)

    print(f"Dados salvos com sucesso em '{nome_arquivo_saida}'")

# Nome do arquivo contendo os códigos dos órgãos
nome_arquivo_codigos_orgaos = "tirando repetidos.json"

# Nome do arquivo de saída
nome_arquivo_saida = "dados_licitacoes_totais.json"

# Executa a função para buscar e salvar os dados
buscar_dados_licitacoes(nome_arquivo_codigos_orgaos, nome_arquivo_saida)
