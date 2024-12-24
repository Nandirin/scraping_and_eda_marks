from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import csv 


load_dotenv()
DNI = os.getenv('DNI')
PASSWORD = os.getenv('PASSWORD')
URL = "https://intranet.upv.es/pls/soalu/est_intranet.ni_portal_n?P_IDIOMA=c"


## Acceder a la sección de notas con Selenium ##
driver = webdriver.Chrome()
driver.get(URL)

dni_box = driver.find_element(by=By.NAME, value='dni')
dni_box.send_keys(DNI)

psswd_box = driver.find_element(by=By.NAME, value='clau')
psswd_box.send_keys(PASSWORD)

enter = driver.find_element(by=By.CLASS_NAME, value='upv_btsubmit')
enter.click()

intranet = driver.find_element(by=By.CLASS_NAME, value='titularEspecial')
intranet.click()

notas = driver.find_element(by=By.CSS_SELECTOR, value='a[title="ir a Notas"]')
notas.click()

nota_ces = driver.find_elements(
    by=By.CSS_SELECTOR, 
    value='a[class="upv_enlacelista"]'
    )[7]
nota_ces.click()


## Scraping de las notas con BeautifulSoup ##
HTML = driver.page_source
soup = BeautifulSoup(HTML, 'html.parser')

tabla_notas = soup.find('table', class_='upv_listacolumnas')
dic_notas_html = tabla_notas.find_all('tr')[1:]

dic_nombres_y_notas = {}
notas = []
nombres = []

for persona in dic_notas_html:
    nombre_nota = persona.find_all('td')
    
    nota = nombre_nota[1].text.replace(',', '.')
    notas.append(float(nota))
    
    nombre = nombre_nota[0].text
    nombres.append(nombre)
    
    dic_nombres_y_notas['nombre'] = nombres
    dic_nombres_y_notas['nota'] = notas


## Crear archivo csv para guardar las notas ##
with open('notas_ces_p.csv', mode='w', newline='', encoding='utf-8') as archivo:
    escritor = csv.writer(archivo)
    
    escritor.writerow(dic_nombres_y_notas.keys())
    
    filas = zip(*dic_nombres_y_notas.values())
    escritor.writerows(filas)


driver.implicitly_wait(3.5)
driver.close()