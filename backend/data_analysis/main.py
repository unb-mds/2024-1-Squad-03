# -*- coding: latin1 -*-
import csv
import json
import os

def analyse_licitacoes(file_path, selected_columns):
    data = []
    try:
        with open(file_path, 'r', encoding='latin1') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for line in csv_reader:
                if (line['Munic�pio'] == "BRASILIA" and 
                    line['Modalidade Compra'] == "Preg�o - Registro de Pre�o" and 
                    line['Valor Licita��o'] != "0,00"):
                    
                    filtered_line = {key: line[key] for key in selected_columns}
                    data.append(filtered_line)
    except FileNotFoundError:
        print("The file does not exist.")
    return data

def save_json(data):
    json_file = "output.json"
    if data:
        mode = 'a' if os.path.exists(json_file) else 'w'
        with open(json_file, mode, encoding='latin1') as file:
            if mode == 'a' and os.path.getsize(json_file) > 1:
                file.write(',')
            json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    folder_path = "licitacoes"  
    selected_columns = [
        "N�mero Licita��o", "Nome UG", 
        "Modalidade Compra", 
        "N�mero Processo", "Objeto", "Situa��o Licita��o", 
        "Nome �rg�o Superior", 
        "Nome �rg�o", "UF", "Munic�pio", 
        "Data Resultado Compra", "Data Abertura", "Valor Licita��o"
    ]

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            data = analyse_licitacoes(file_path, selected_columns)
            save_json(data)

if __name__ == "__main__":
    main()
