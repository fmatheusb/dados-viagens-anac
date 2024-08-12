import os
import zipfile
import pandas as pd
import csv

# Caminho da pasta com os arquivos zip
caminho_pasta = r"C:\Users\fmath\Documents\dados-viagens-anac\dados-viagens-anac\data\arquivos_brutos"

# Caminho final para o csv tratado
caminho_final = r"C:\Users\fmath\Documents"

# Lista para armazenar os DataFrames
lista_df = []

# Contar todos os arquivos ZIP na pasta
total_zips = sum([1 for arquivo in os.listdir(caminho_pasta) if arquivo.endswith('.zip')])

# Contador de arquivos processados
arquivos_processados = 0

# Loop através de cada arquivo na pasta
for arquivo in os.listdir(caminho_pasta):
    if arquivo.endswith('.zip'):
        caminho_zip = os.path.join(caminho_pasta, arquivo)
        
        # Abre o arquivo zip
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            # Lista todos os arquivos no zip
            for nome_arquivo in zip_ref.namelist():
                if (nome_arquivo.endswith('.CSV') or nome_arquivo.endswith('.csv')):
                    # Extrai o arquivo CSV para um DataFrame temporário
                    with zip_ref.open(nome_arquivo) as csvfile:
                        try:
                            # Tente ler o CSV detectando automaticamente o separador (padrão de arquivos até 2019)
                            df_temp = pd.read_csv(csvfile, encoding='ISO-8859-1', sep=None, engine='python'
                                                  , usecols=['ANO', 'MES', 'EMPRESA', 'ORIGEM', 'DESTINO', 'TARIFA', 'ASSENTOS'])
                            lista_df.append(df_temp)
                            print(df_temp.columns, nome_arquivo)

                        except Exception:
                            try:
                                #Leitura do segundo padrão de dados
                                df_temp = pd.read_csv(csvfile, encoding='latin', sep=';', engine='python',skiprows=1)
                                df_temp.columns = ['ANO', 'MES', 'EMPRESA', 'ORIGEM', 'DESTINO', 'TARIFA', 'ASSENTOS']
                                lista_df.append(df_temp)

                            except Exception as e:
                                try:
                                    #Leitura do terceiro padrão de dados
                                    df_temp = pd.read_csv(csvfile, encoding='latin', sep=';', engine='python')

                                    #Ajuste de colunas
                                    df_temp.columns = ['REMOVER','ANO', 'MES', 'EMPRESA', 'ORIGEM', 'DESTINO', 'TARIFA', 'ASSENTOS']

                                    # #Tratando os dados da coluna para padronizar as informações
                                    # df_temp.rename(columns={'Ano de Referência': 'ANO',
                                    #                         'Mês de Referência': 'MES',
                                    #                         'ICAO Empresa Aérea': 'EMPRESA',
                                    #                         'ICAO Aeródromo Origem': 'ORIGEM',
                                    #                         'ICAO Aeródromo Destino': 'DESTINO',
                                    #                         'Tarifa-N': 'TARIFA',
                                    #                         'Assentos Comercializados': 'ASSENTOS'}, inplace=True)
                                    
                                    # Trazendo apenas as colunas necessárias
                                    df_temp = df_temp.loc[:, ['ANO', 'MES', 'EMPRESA', 'ORIGEM', 'DESTINO', 'TARIFA', 'ASSENTOS']]
                                    lista_df.append(df_temp)
                                
                                except Exception as e:
                                    print(f'Erro ao ler {nome_arquivo} em {arquivo}: {e}')
                                    teste = pd.read_csv(csvfile, encoding='utf-16', sep=';', engine='python', nrows=5)
                                    print(f"Nomes das colunas no segundo padrão em {nome_arquivo}: {teste.columns.to_list()}")
                                    # print(pd.read_csv(csvfile, encoding='ISO-8859-1', sep=';').head())
                                    # print(nome_arquivo)
                                    teste1 = pd.read_csv(csvfile, encoding='utf-8', sep=';', engine='python')
                                    print(pd.read_csv(csvfile, encoding='latin', sep=None, engine='python').columns.to_list())
                                    # print(pd.read_csv(csvfile, encoding='latin', sep=';', engine='python', nrows=10).head())
                                    # print(e)

    #Atualizando contador
    percentual_conclusao = (arquivos_processados/total_zips) * 100
    arquivos_processados += 1
    print(f"Finalizando arquivo {arquivos_processados} de {int(total_zips)} ({percentual_conclusao:.0f}%)")

# Concatena todos os DataFrames em um único DataFrame
df_final = pd.concat(lista_df, ignore_index=True)

# Ajusta o nome das colunas
df_final.columns = [col.lower() for col in df_final.columns]

# Tratando os dados da coluna de tarifa
df_final['tarifa'] = df_final['tarifa'].str.replace(',', '.')

# Converte todas as colunas para string se necessário
df_final = df_final.astype({col: 'str' for col in df_final.select_dtypes(include=['object']).columns})

# Envia o dataframe tratado para uma pasta
df_final.to_parquet(f"{caminho_final}\\base_anac_tratada.parquet", index=False)