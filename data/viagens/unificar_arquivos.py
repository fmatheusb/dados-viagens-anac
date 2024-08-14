import os
import zipfile
import pandas as pd
import shutil
import re
import chardet
import io

# Caminho da pasta com os arquivos zip
caminho_pasta = r"C:\Users\fmath\Documents\dados-viagens-anac\dados-viagens-anac\data\arquivos_brutos"

# Caminho final para o csv tratado
caminho_final = r"C:\Users\fmath\Documents"

# Pasta temporária para descompactar os arquivos
pasta_temporaria = r"C:\Users\fmath\Documents\dados-viagens-anac\dados-viagens-anac\data\temp"

# Lista para armazenar os DataFrames
lista_df = []

# Contador de arquivos processados
arquivos_processados = 0

# Os arquivos possuem encode diferente. Vamos tratá-los para evitar problemas com isso
def detectar_encoding(caminho_arquivo, amostra_tamanho=10000):
    with open(caminho_arquivo, 'rb') as f:
        resultado = chardet.detect(f.read(amostra_tamanho))
    return resultado['encoding']

# Loop através de cada arquivo na pasta
for arquivo in os.listdir(caminho_pasta):
    if arquivo.endswith('.zip'):
        caminho_zip = os.path.join(caminho_pasta, arquivo)

        # Descompactar o arquivo ZIP para a pasta temporária
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall(pasta_temporaria)

# Avisando que todos os arquivos zips foram lidos
print("Leitura dos arquivos zip finalizada com sucesso")

# Contar todos os arquivos CSV na pasta
total_csv = sum([1 for arquivo in os.listdir(pasta_temporaria) if arquivo.endswith('.csv') or arquivo.endswith('CSV')])

# Lista todos os arquivos descompactados
for nome_arquivo in os.listdir(pasta_temporaria):
    if nome_arquivo.endswith('.CSV') or nome_arquivo.endswith('.csv'):
        caminho_csv = os.path.join(pasta_temporaria, nome_arquivo)

        # Detectar o encode do arquivo
        encoding_detectado = detectar_encoding(caminho_csv)

        # Ler o conteúdo
        with open(caminho_csv, 'r', encoding=encoding_detectado) as f:
            conteudo_str = f.read()
        
        try:
            # Tente ler o CSV detectando automaticamente o separador (padrão de arquivos até 2019)
            df_temp = pd.read_csv(io.StringIO(conteudo_str), encoding='utf-8', sep=None, engine='python'
                                    , usecols=['ANO', 'MES', 'EMPRESA', 'ORIGEM', 'DESTINO', 'TARIFA', 'ASSENTOS'])
            lista_df.append(df_temp)
            print(f"Arquivo {nome_arquivo} lido com sucesso. Tipo 1")
        
        except:
            try:
                #Lê o arquivo CSV com o encoding e delimitador corretos
                df_temp = pd.read_csv(io.StringIO(conteudo_str), encoding='utf-8', sep=';', engine='python')

                # Renomeia as colunas para padronizar
                df_temp.rename(columns={'Ano de Referência': 'ANO',
                                        'Mês de Referência': 'MES',
                                        'ICAO Empresa Aérea': 'EMPRESA',
                                        'ICAO Aeródromo Origem': 'ORIGEM',
                                        'ICAO Aeródromo Destino': 'DESTINO',
                                        'Tarifa-N': 'TARIFA',
                                        'Assentos Comercializados': 'ASSENTOS'}, inplace=True)

                # Seleciona as colunas corretas para igualar os dois dataframes
                df_temp = df_temp.loc[:, ['ANO', 'MES', 'EMPRESA', 'ORIGEM', 'DESTINO', 'TARIFA', 'ASSENTOS']]


                lista_df.append(df_temp)
                print(f"Arquivo {nome_arquivo} lido com sucesso. Tipo 2")

            except Exception as e:
                print(f'Erro ao ler {nome_arquivo}: {e}')

    # Atualizando contador
    arquivos_processados += 1
    percentual_conclusao = (arquivos_processados / total_csv) * 100
    print(f"Finalizando arquivo {arquivos_processados} de {int(total_csv)} ({percentual_conclusao:.0f}%)")

# Concatena todos os DataFrames em um único DataFrame
df_final = pd.concat(lista_df, ignore_index=True)

# Ajusta o nome das colunas para minúsculas
df_final.columns = [col.lower() for col in df_final.columns]

# Tratando os dados da coluna de tarifa
df_final['tarifa'] = df_final['tarifa'].str.replace(',', '.').astype(float)

# Envia o dataframe tratado para uma pasta
df_final.to_parquet(f"{caminho_final}\\base_anac_tratada.parquet", index=False)

# Limpar a pasta temporária
shutil.rmtree(pasta_temporaria)