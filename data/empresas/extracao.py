from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Caminho do diretório temporário
temp_dir = r"C:\Users\fmath\Documents\dados-viagens-anac\dados-viagens-anac\data\empresas\arquivos_brutos"

# Função para limpar todos os arquivos .zip do diretório
def clear_zip_files(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith(".zip"):
            file_path = os.path.join(directory, file_name)
            try:
                os.remove(file_path)
                print(f"Arquivo removido: {file_path}")
            except Exception as e:
                print(f"Erro ao remover {file_path}: {e}")

# Configurar as opções do Chrome
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": temp_dir,
    "download.prompt_for_download": False,  # Desabilitar prompt de download
    "directory_upgrade": True,  # Atualizar o diretório se ele já existe
})

# Iniciar o WebDriver com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)

# Acessar a página
driver.get("https://sas.anac.gov.br/sas/downloads/view/frmDownload.aspx?tema=13")

# Limpar arquivos .zip antes de iniciar
clear_zip_files(temp_dir)

# Seleciona todos os anos disponíveis
select_element = Select(driver.find_element(By.ID, 'MainContent_listAno'))
anos = [option.get_attribute('value') for option in select_element.options]

# Iterar sobre cada ano
for ano in anos:

    # Reencontrar o elemento de ano e clicar nele
    ano_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//option[@value='{ano}']")))
    ano_element.click()
    
    # Clicar no botão "Buscar Arquivos"
    buscar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'MainContent_btnListaArquivos')))
    buscar_button.click()
    
    # Esperar até que a lista de arquivos seja carregada
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'MainContent_btnMarcar')))
    
    # Clicar no botão "Marcar Todos"
    marcar_todos_button = driver.find_element(By.ID, 'MainContent_btnMarcar')
    marcar_todos_button.click()
    
    # Clicar no botão "Baixar Marcados"
    baixar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'MainContent_btnBaixar')))
    baixar_button.click()

#Tempo para finalizar todos os downloads
time.sleep(80)

# Fechar o navegador
driver.quit()