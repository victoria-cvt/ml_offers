import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Configuração do driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Acessa o site
driver.get("https://www.mercadolivre.com.br/ofertas#nav-header")
time.sleep(5)

# Captura o container principal e os itens dentro dele
container = driver.find_element(By.XPATH, '//*[@id="root-app"]/div/section/div/div')
items = container.find_elements(By.XPATH, './div')[:10]  # Captura os primeiros 10 elementos

offers = []

# Itera sobre os primeiros 10 itens encontrados
for item in items:
    try:
        # Busca os dados relativos ao item atual
        title = item.find_element(By.XPATH, './/div[2]/a').text
        price = item.find_element(By.XPATH, './/div[2]/div[1]/div/span[1]').text
        discount = item.find_element(By.XPATH, './/div[2]/div[1]/div/span[2]').text

        # Adiciona os dados à lista
        offers.append({
            'Item:': title,
            'Por apenas:': price,
            'Desconto de:': discount
        })

    except Exception as e:
        print(f"Erro ao capturar dados de um item: {e}")

# Fecha o navegador
driver.quit()

# Salva os dados em um arquivo Excel
if offers:
    df = pd.DataFrame(offers)
    df.to_('itens_promocao.xlsx', index=False)
    print("Dados salvos com sucesso.")
else:
    print("Nenhuma oferta encontrada.")
