from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys

def research (canasta_basica,info):
    
    for store in info:
        
        for prod in canasta_basica:
            service = Service(ChromeDriverManager().install())
            option = webdriver.ChromeOptions()
            #option.add_argument("--headless")

            #Open the website
            option.add_argument("--window-size=1920,1800")
            driver = Chrome(service=service,options=option)
            driver.get(info[store][0])
            options = webdriver.ChromeOptions()
            options.page_load_strategy = 'normal'  # espera hasta que la página cargue
            #Creting empty df
            products_data = []
            product_names_seen = set()  # Set to keep track of unique product names
            #Search the product
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,info[store][4]).send_keys(canasta_basica[prod])
            options.page_load_strategy = 'normal'  # espera hasta que la página cargue
            driver.find_element(By.CSS_SELECTOR,info[store][5]).click()
            options.page_load_strategy = 'normal'  # espera hasta que la página cargue



            #Getting prices

            last_height = driver.execute_script("return document.body.scrollHeight")
            '''products_collected = 0  # Variable para contar los productos recopilados
            max_products = 3  # Número máximo de productos a recopilar'''
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # Desplazarse hacia abajo en pequeños intervalos
                driver.execute_script("window.scrollBy(0, 600);")
                time.sleep(2)  # Esperar para cargar los productos

                # Comprobar los productos después de desplazarse
                
                cards_found = driver.find_elements(By.CSS_SELECTOR, info[store][1])
                    
                for card in cards_found:
                    try:        
                        name_element = card.find_element(By.CSS_SELECTOR, info[store][3])
                        price_element = card.find_element(By.CSS_SELECTOR, info[store][2])
                        name_element = name_element.text
                        price_element = price_element.text
                        price_element = float(price_element.replace('$', '').replace('.', '').replace(',', '.'))
                        #Print(name_element,price_element)


                        # Verificar si ya hemos visto este producto
                        if name_element not in product_names_seen:
                            products_data.append({"Product Name": name_element, "Price": price_element, "Store": store})
                            product_names_seen.add(name_element)  # Añadir el nombre del producto al set
                    
                    except :
                        
                        products_data.append({"Product Name": "El producto no se encontró", "Price": 0, "Store": store})
                        '''products_collected = max_products'''
                        break
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:  
                    break
                last_height = new_height
            driver.quit()
            from insert import insert
            final_df = pd.DataFrame(products_data)
            insert(final_df , prod)

    

    df = pd.DataFrame(products_data)
    
    return df 