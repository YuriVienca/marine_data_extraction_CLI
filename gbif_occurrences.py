# -*- coding: utf-8 -*-
"""
Este programa extrai os registros de ocorrência de determinada espécie marinha 
da plataforma 'Global Biodiversity Information Facility' (GBIF), gerando um 
arquivo csv com os dados de Longitude(decimal), Latitude(decimal), ano, dia e 
mês de ocorrência. 

Entrada: 
  - Nome científico da espécie (--species 'Xxxxxx xxxxx')
  - Limites geográficos de busca (--bbox '-90.0 90.0 -180.0 180.0')
  - Limite do número de ocorrências (--limit XXX)
  - Data de início (--begin_date 'YYYY-MM-DD')
  - Data final (--end_date 'YYYY-MM-DD')
  - Nome do arquivo CSV de saída (--out_csv 'example.csv')

Vale ressaltar que os limites geográficos devem ser informados na forma a seguir: 
lat_min lat_max lon_min lon_max (sempre do menor para o maior). Ademais,o limite 
máximo para requisições nesse API é de 300, priorizando os dados mais recentes 
e os ordenando cronologicamente.  

Autor: Yuri Encarnação Data: Abril/2025
"""

from pygbif import species as spp
from pygbif import occurrences as occ
import argparse
import csv

def main():
    
    # Obtém os argumentos da CLI
    args = args_cli()
    
    # Busca dados no GBIF
    data = gbif_search(args.species, args.bbox, args.limit, args.begin_date, args.end_date)
    
    # Se houver dados, salva no CSV
    if data:
        csv_save(args.out_csv, data)
        print("Dados de ocorrências gravados com sucesso!")
    else:
        print("Nenhum dado de ocorrência encontrado para os parâmetros informados.")
        
    
# Função para delimitar os argumentos da linha de comando
def args_cli():
    
    args = argparse.ArgumentParser(description="Chaves para o CLI")
    args.add_argument('--species', required=True, help="Nome da espécie para pesquisa no GBIF.")
    args.add_argument('--bbox', required=True, help="Limites geográficos para a pesquisa (ex: '-90 90 -180 180')")
    args.add_argument('--limit', type=int, help="Limite de registros a serem retornados, sendo o máximo 300")
    args.add_argument('--begin_date', required=True, help="Data de início (YYYY-MM-DD)")
    args.add_argument('--end_date', required=True, help="Data de término (YYYY-MM-DD)")
    args.add_argument('--out_csv', required=True, help="Nome do arquivo CSV de saída")
    
    return args.parse_args()


# Função para buscar os dados de ocorrência no GBIF
def gbif_search(species, bbox, limit, begin_date, end_date):
    
    
    # Corverte a string bbox em uma lista de coordenadas
    box = bbox.split()                           
    lat_min, lat_max, lon_min, lon_max = box        

    # Obtém a chave taxonômica, caso tenha, evitando ambiguidades e problemas com sinônimos 
    key = spp.name_backbone(name = species, rank='species')['usageKey']
    
    # Realiza a busca no GBIFpara ocorrências com coordenadas
    if key:
        occur = occ.search(
            taxonKey = key, 
            decimalLatitude = f'{lat_min},{lat_max}', 
            decimalLongitude = f'{lon_min},{lon_max}', 
            eventDate= f'{begin_date},{end_date}',
            hasCoordinate=True, 
            limit = limit)  

    # Caso não tenha chave taxonômica, se utiliza diretamente o nome    
    else:
        occur = occ.search(
            scientificName = species, 
            decimalLatitude = f'{lat_min},{lat_max}', 
            decimalLongitude = f'{lon_min},{lon_max}', 
            eventDate= f'{begin_date},{end_date}',
            hasCoordinate=True, 
            limit = limit)             


    # Processa e armazena os dados em uma lista
    data = []
    for x in occur['results']: 
        
        # Filtra dados sem data completa ou com mais de uma data para mesma ocorrência
        # Ambos os casos não possuem o argumento 'day' no banco de dados
        if 'day' in x:  
            longitude = f"{float(x['decimalLongitude']):.4f}"
            latitude = f"{float(x['decimalLatitude']):.4f}"
            year = int(x['year'])
            month = int(x['month'])
            day = int(x['day'])
            
            #Evita valores duplicados
            if [longitude, latitude, year, day, month] not in data:
                data.append([longitude, latitude, year, day, month])
      
    # Ordena os dados cronologicamente           
    data.sort(key=lambda x: (x[2],x[4],x[3]))
    
    return data

    
# Função para salvar os dados em um arquivo CSV
def csv_save(filename, data):
   with open(filename, mode='w', newline='') as file:
       writer = csv.writer(file)
       writer.writerow(["decimalLongitude", "decimalLatitude", "year", "day", "month"])
       writer.writerows(data) 

    
main()