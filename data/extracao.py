from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import pandas as pd
import time

# Configuração do webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Acessar a página
driver.get("https://sas.anac.gov.br/sas/downloads/view/frmDownload.aspx?tema=14")

# Espera para garantir que a página carregue
time.sleep(2)

# Seleciona todos os anos disponíveis
select_element = Select(driver.find_element(By.ID, 'MainContent_listAno'))
anos = [option.get_attribute('value') for option in select_element.options]

# Lista para armazenar dataframes
dataframes = []

# Iterar sobre cada ano
for ano in anos:
    # Reencontrar o elemento de ano e clicar nele
    ano_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//option[@value='{ano}']")))
    ano_element.click()
    
    # Clicar no botão "Buscar Arquivos"
    buscar_button = driver.find_element(By.ID, 'MainContent_btnListaArquivos')
    buscar_button.click()
    
    # Espera para garantir que os arquivos carreguem
    time.sleep(2)
    
    # Clicar no botão "Marcar Todos"
    marcar_todos_button = driver.find_element(By.ID, 'MainContent_btnMarcar')
    marcar_todos_button.click()
    
    # Clicar no botão "Baixar Marcados"
    baixar_button = driver.find_element(By.ID, 'MainContent_btnBaixar')
    baixar_button.click()
    
    # Espera para garantir o download dos arquivos
    time.sleep(10)  # Ajuste conforme necessário para garantir que os arquivos sejam baixados

    # Verifica a pasta de downloads
    download_dir = 'data/arquivos'  # Substitua pelo caminho correto da pasta de downloads
    downloaded_files = [os.path.join(download_dir, file) for file in os.listdir(download_dir) if file.endswith(".csv")]
    
    # Carregar os arquivos CSV e armazená-los em uma lista de dataframes
    for file in downloaded_files:
        df = pd.read_csv(file)
        dataframes.append(df)
    
    # Opcional: mover os arquivos para uma pasta temporária ou deletar após o uso
    for file in downloaded_files:
        os.remove(file)  # Remove o arquivo após processamento

# Concatenar todos os dataframes em um único CSV
final_df = pd.concat(dataframes, ignore_index=True)
final_df.to_csv("output.csv", index=False)

# Fechar o navegador
driver.quit()
