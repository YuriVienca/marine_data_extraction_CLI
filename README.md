
# 🌊 Marine Data CLI Tools

Este repositório contém duas ferramentas em Python desenvolvidas para auxiliar na coleta e processamento de dados ambientais marinhos:

1. **Extração de dados de ocorrência de espécies marinhas via GBIF**
2. **Extração de temperatura e salinidade da superfície do mar via Copernicus Marine Service (CMEMS)**

---

## 📁 Estrutura do Projeto

```
marine-data-cli/
├── gbif_occurrences.py       # Script para extrair dados de ocorrência do GBIF
├── cmems_parameters.py       # Script para extrair temperatura e salinidade do CMEMS
├── requirements.txt          # Lista de dependências Python
├── chelonia_mydas_occur.csv  # Exemplo de saída para o script do GBIF
├── c_mydas_parameters.csv    # Exemplo de saída para o script do CMEMS
└── README.md                 # Este arquivo
```

---

## 1️⃣ Extração de Ocorrências via GBIF

### 📌 Descrição

Este script acessa a plataforma [GBIF](https://www.gbif.org/) e retorna um arquivo CSV com registros de ocorrência de uma espécie marinha, incluindo latitude, longitude, ano, mês e dia.

### ⚙️ Uso

```bash
python gbif_occurrences.py 
  --species "Nome científico" 
  --bbox "lat_min lat_max lon_min lon_max" 
  --limit 300 
  --begin_date "YYYY-MM-DD" 
  --end_date "YYYY-MM-DD" 
  --out_csv "saida.csv"
```

### 📥 Exemplo

```bash
python gbif_occurrences.py --species "Thunnus albacares" --bbox "-30 -10 -50 -30" --limit 10 --begin_date "2010-01-01" --end_date "2020-12-31" --out_csv "thunnus_ocorrencias.csv"
```

---

## 2️⃣ Extração de Dados do CMEMS

### 📌 Descrição

Este script utiliza a plataforma [Copernicus Marine Service](https://marine.copernicus.eu/) para extrair dados de temperatura (°C) e salinidade (UPS) na profundidade de 0.5m, com base em um arquivo CSV de entrada contendo coordenadas e datas.

### ⚙️ Pré-requisitos

Você precisa estar autenticado no `copernicusmarine` antes de rodar o script:

```python
copernicusmarine.login(username='seu_usuario', password='sua_senha')
```

> A autenticação pode ser feita uma única vez no seu ambiente local.

---

### ⚙️ Uso

```bash
python cmems_extraction.py --csv "entrada.csv" --out_csv "saida.csv"
```

### 📥 Formato do CSV de entrada

```csv
decimalLongitude,decimalLatitude,year,day,month
-40.1234,-20.5678,2020,15,6
-41.1234,-21.5678,2021,12,9
```

---

## 💻 Requisitos

Instale os pacotes necessários com:

```bash
pip install -r requirements.txt
```

**`requirements.txt`**:

```
pygbif
copernicusmarine

```

---

## 👨‍💻 Autor

**Yuri Encarnação**  
Abril / 2025


