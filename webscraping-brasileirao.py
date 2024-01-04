
# Importando bibliotecas necessárias
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json

# Coletando o conteúdo HTML a partir da URL na página da CBF
url = "https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a" 

# Configurando as opções do Chrome
options = Options()
options.headless = True  # Defina como False se deseja abrir o navegador visivelmente

# Inicializando o driver do Chrome com as opções usando webdriver_manager
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

# Acessando a URL
driver.get(url)

# Buscando os elementos da tabela dentro da página web
element = driver.find_element_by_xpath("//div[@class='col-md-8 col-lg-9']//table")
html_content = element.get_attribute('outerHTML')

# Parseando o conteudo do HTML - BeaultifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

# Estruturando o conteudo em um dataframe
df_full = pd.read_html(str(table))[0]
df = df_full [['Posição', 'PTS', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG', 'CA', 'CV', '%']]

# Excluindo linhas com valores vazios
df = df.dropna()

# Exibir as colunas disponíveis no DataFrame
# print(df_full.columns)

# Transformandos os dados em um dicionário de dados
ranking = {}
ranking['classificacao'] = df.to_dict('records')


# Certifique-se de fechar o driver quando não precisar mais
driver.quit()

# Convertendo e salvando em um arquivo JSON
js = json.dumps(ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close()
