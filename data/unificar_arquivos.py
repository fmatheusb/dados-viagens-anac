import os
import zipfile
import pandas as pd
import csv

# Caminho da pasta com os arquivos zip
caminho_pasta = r"C:\Users\fmath\Documents\dados-viagens-anac\dados-viagens-anac\data\arquivos_brutos"

# Caminho final para o csv tratado
caminho_final = r"C:\Users\fmath\Documents\dados-viagens-anac\dados-viagens-anac\data\arquivo_tratado"

# Lista para armazenar os DataFrames
lista_df = []

# Loop através de cada arquivo na pasta
for arquivo in os.listdir(caminho_pasta):
    if arquivo.endswith('.zip'):
        caminho_zip = os.path.join(caminho_pasta, arquivo)
        
        # Abre o arquivo zip
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            # Lista todos os arquivos no zip
            for nome_arquivo in zip_ref.namelist():
                if nome_arquivo.endswith('.CSV'):
                    # Extrai o arquivo CSV para um DataFrame temporário
                    with zip_ref.open(nome_arquivo) as csvfile:
                        df_temp = pd.read_csv(csvfile, encoding='latin1', sep=';')
                        lista_df.append(df_temp)

# Concatena todos os DataFrames em um único DataFrame
df_final = pd.concat(lista_df, ignore_index=True)

# Envia o dataframe tratado para uma pasta
df_final.to_csv(f"{caminho_final}\\base_anac_tratada.csv")