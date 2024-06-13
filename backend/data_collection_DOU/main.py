import argparse
import functions as fs
from datetime import datetime

def processa_licitacoes(mes_inicial, ano_inicial, mes_final, ano_final):
    for i in range(ano_inicial, ano_final + 1):
        primeiro_mes = mes_inicial if i == ano_inicial else 1
        ultimo_mes = mes_final if i == ano_final else 12
        for j in range(primeiro_mes, ultimo_mes + 1):
            fs.processa_xml_licitacoes(
                fs.processa_xml_obtem_brasilia(
                    fs.faz_download_do_zip(
                        fs.captura_link_banco_de_dados_DOU_mes(i, j), i, j
                    )
                )
            )

def main():
    parser = argparse.ArgumentParser(description='Processa licitações DOU')
    parser.add_argument('inicio', nargs='?', help='Data inicial no formato mm/aaaa')
    parser.add_argument('fim', nargs='?', help='Data final no formato mm/aaaa')

    args = parser.parse_args()
    
    ano_atual = datetime.now().year
    mes_atual = datetime.now().month

    if args.inicio and args.fim:
        try:
            mes_inicial, ano_inicial = map(int, args.inicio.split('/'))
            mes_final, ano_final = map(int, args.fim.split('/'))

            # Verificação básica para garantir que as datas são válidas
            if not (1 <= mes_inicial <= 12 and 1 <= mes_final <= 12):
                raise ValueError('Os meses devem estar entre 1 e 12.')
            if ano_inicial > ano_final or (ano_inicial == ano_final and mes_inicial > mes_final):
                raise ValueError('A data inicial deve ser anterior ou igual à data final.')

            processa_licitacoes(mes_inicial, ano_inicial, mes_final, ano_final)
        except ValueError as ve:
            print(f'Erro nos argumentos: {ve}')
    else:
        # Sem argumentos, processa conforme lógica original
        if mes_atual == 1:
            for i in range(2002, ano_atual):
                for j in range(1, 13):
                    fs.processa_xml_licitacoes(
                        fs.processa_xml_obtem_brasilia(
                            fs.faz_download_do_zip(
                                fs.captura_link_banco_de_dados_DOU_mes(i, j), i, j
                            )
                        )
                    )
        else:
            for i in range(2002, ano_atual + 1):
                ultimo_mes = 12 if i < ano_atual else mes_atual - 1
                for j in range(1, ultimo_mes + 1):
                    fs.processa_xml_licitacoes(
                        fs.processa_xml_obtem_brasilia(
                            fs.faz_download_do_zip(
                                fs.captura_link_banco_de_dados_DOU_mes(i, j), i, j
                            )
                        )
                    )

if __name__ == '__main__':
    main()