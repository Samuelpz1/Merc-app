from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import mysql.connector
num_pages = 10

def main():
    #Store , link , cards , price , name
    info = {
        'Jumbo': ('https://www.tiendasjumbo.co/supermercado/despensa' , 'div.tiendasjumboqaio-cmedia-integration-cencosud-0-x-galleryItem' , 'div.tiendasjumboqaio-jumbo-minicart-2-x-price','span.vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName'),
        'Exito': ('https://www.exito.com/mercado/despensa', 'article.productCard_productCard__M0677','.ProductPrice_container__price__XmMWA','.styles_name__qQJiK'),
        'D1': ('https://domicilios.tiendasd1.com/ca/alimentos-y-despensa/ALIMENTOS%20Y%20DESPENSA', 'div.styles__StyledCard-sc-3jvmda-0','p.CardBasePrice__CardBasePriceStyles-sc-1dlx87w-0','p.CardName__CardNameStyles-sc-147zxke-0'),
        'Vaquita': ('https://lavaquita.co/collections/despensa','.productitem','.productitem .price--main .money', '.productitem .productitem--title')
        
    }
    #research()
    '''for store in info:
        research(store ,info[store][0], info[store][1],info[store][2], info[store][3])'''
    research('Vaquita' ,info['Vaquita'][0], info['Vaquita'][1],info['Vaquita'][2], info['Vaquita'][3])

def research (store , link , cards , price , name):
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    #option.add_argument("--headless")

    #Open the website
    option.add_argument("--window-size=1920,1800")
    driver = Chrome(service=service,options=option)
    driver.get(link)
    time.sleep(20)

    #Creting empty df
    products_data = []
    product_names_seen = set()  # Set to keep track of unique product names


    #Getting prices

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Desplazarse hacia abajo en pequeños intervalos
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)  # Esperar para cargar los productos

        # Comprobar los productos después de desplazarse
        cards_found = driver.find_elements(By.CSS_SELECTOR, cards)

        for card in cards_found:
            name_element = card.find_element(By.CSS_SELECTOR, name)
            price_element = card.find_element(By.CSS_SELECTOR, price)
            name_element = name_element.text
            price_element = price_element.text
            price_element = float(price_element.replace('$', '').replace('.', '').replace(',', '.'))
            print(name_element,price_element)


            # Verificar si ya hemos visto este producto
            if name_element not in product_names_seen:
                products_data.append({"Product Name": name_element, "Price": price_element, "Store": store})
                product_names_seen.add(name_element)  # Añadir el nombre del producto al set

        # Scroll incremental hacia abajo
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)

        # Verificar si llegamos al final de la página
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()

    df = pd.DataFrame(products_data)
    
    db_connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Test01',
        database = 'mercapp'

    )

    cursor = db_connection.cursor()

    for index, row in df.iterrows():
        sql = 'INSERT INTO precio_producto (product_name , product_price , store) VALUES (%s, %s , %s)'
        values = (row['Product Name'], row['Price'], row['Store'])
        cursor.execute(sql, values)

    db_connection.commit()
    print(f"{cursor.rowcount} registros insertados.")

    # Cerrar la conexión
    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()