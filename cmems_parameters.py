# -*- coding: utf-8 -*-
"""
Este programa extrai dados de temperatura (thetao) e salinidade (so) da água em
diversos pontos, utilizando informações disponibilizadas pela plataforma 
Copernicus Marine Service (CMEMS). Os dados são extraídos a partir de um arquivo 
CSV de entrada, no qual cada linha deve conter os seguintes campos separados por 
vírgulas: decimalLongitude, decimalLatitude, year, day, month. Vale ressaltar 
que a primeira linha será considerada como título. 

Entrada: 
    - Nome do arquivo de entrada (--csv 'XXXX.csv')
    - Nome do arquivo de saída (--out_csv 'XXXXXX.csv')

Como saída, o programa gera um novo arquivo CSV com o nome especificado pelo 
usuário. Esse arquivo mantém a estrutura original, adicionando as colunas de 
temperatura(C) e salinidade(UPS) ao final de cada linha. Para o processamento, será
considerada a profundidade de 0.5m(superfície), o mínimo do CMEMS. O código 
também considera que o usuário já esteja autenticado. 

(copernicusmarine.login(username='<your_username>', password='<your_password>'))

Autor: Yuri Encarnação Data: Abril/2025

"""
import copernicusmarine
import csv
import argparse
from datetime import datetime
import math

def main():
    
    # Obtém os argumentos da CLI
    args = args_cli()
    
    # Busca dados no CMEMS
    data = cmems_search(args.csv)
    
    csv_save(args.out_csv, data)
    print("Dados gravados com sucesso!")
    

# Função para delimitar os argumentos da linha de comando    
def args_cli():
    
    args = argparse.ArgumentParser(description="Chaves para o CLI")
    args.add_argument('--csv', required=True, help= "Nome do arquivo CSV de entrada")
    args.add_argument('--out_csv', required=True, help= "Nome do arquivo CSV de saída")
    
    return args.parse_args()


# Função para buscar os dados de temperatura e salinidade no CMEMS
def cmems_search(csv): 
    
    data_list = []
    
    id_old = "cmems_mod_glo_phy_my_0.083deg_P1D-m"  # Banco de dados 01/01/1993→30/06/2021
    id_new = "cmems_mod_glo_phy_myint_0.083deg_P1D-m"# Banco de dados 01/07/2021→25/02/2025
    vr = ['thetao', 'so'] # Temperatura e salinidade
    dp = 0.5 # Profundidade = superfície
    
    # Abre e percorre as linhas do arquivo de entrada
    with open(csv, mode='r', newline='') as file:
        
        for line in file.readlines()[1:]:
            
            lon_str, lat_str, year_str, day_str, month_str = line.strip().split(',')
            lon = float(lon_str)
            lat = float(lat_str)
            year = int(year_str)
            day = int(day_str)
            month = int(month_str)
            date = f"{year:04d}-{month:02d}-{day:02d}"
            date = datetime.strptime(date, "%Y-%m-%d")
            
            if date < datetime(2021, 7, 1): #Data limite entre os datasets
                dataset_id = id_old
            else:
                dataset_id = id_new
            
            # Faz a requisição dos dados para cada ponto no CMEMS
            data = copernicusmarine.open_dataset(
                dataset_id=dataset_id,
                variables=vr,
                maximum_longitude=lon,
                minimum_longitude=lon,
                minimum_latitude=lat,
                maximum_latitude=lat,
                start_datetime=date,
                end_datetime=date,
                maximum_depth=dp,
                minimum_depth=dp)
            
            
            #Retira os valores do array e arredonda para 2 casas decimais
            thetao = round(data['thetao'].values.item(), 2)
            so = round(data['so'].values.item(), 2)
            
            #Ignora as linhas que possuem NaN
            if not (math.isnan(thetao) or math.isnan(so)):
                data_list.append((lon, lat, year, day, month, thetao, so))
            
    return (data_list)

# Função para salvar os dados em outro arquivo CSV
def csv_save(filename, data): 
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["decimalLongitude", "decimalLatitude", "year", "day", "month", "temperature", "salinity"])
        writer.writerows(data) 

main()
