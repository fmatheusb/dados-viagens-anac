from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os

# Configurações do ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Acessa a página alvo
url = "https://sas.anac.gov.br/sas/downloads/view/frmDownload.aspx?tema=14"
driver.get(url)

# Espera a página carregar completamente
time.sleep(5)

# Expande todas as seções de anos, se necessário
anos = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox'][name^='year']")

for ano in anos:
    if not ano.is_selected():
        ano.click()
        time.sleep(2)  # Espera para garantir que os arquivos sejam carregados

# Agora, localiza todos os links de download
links = driver.find_elements(By.CSS_SELECTOR, "a[href*='downloadFile.aspx']")

# Diretório onde os arquivos serão salvos
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Baixa todos os arquivos
for link in links:
    file_url = link.get_attribute('href')
    file_name = link.text.strip()
    file_path = os.path.join('downloads', file_name)

    # Faz o download do arquivo
    response = requests.get(file_url)
    
    # Salva o arquivo localmente
    with open(file_path, 'wb') as file:
        file.write(response.content)
        print(f"Arquivo salvo: {file_name}")

# Fecha o navegador
driver.quit()