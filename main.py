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
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    #option.add_argument("--headless")

    #Open the website
    option.add_argument("--window-size=1920,1800")
    driver = Chrome(service=service,options=option)
    driver.get("https://www.tiendasjumbo.co/supermercado/despensa")
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
        cards = driver.find_elements(By.CSS_SELECTOR, "div.tiendasjumboqaio-cmedia-integration-cencosud-0-x-galleryItem")

        for card in cards:
            name_element = card.find_element(By.CSS_SELECTOR, "span.vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName")
            price_element = card.find_element(By.CSS_SELECTOR, "div.tiendasjumboqaio-jumbo-minicart-2-x-price")
            name = name_element.text
            price = price_element.text
            price = float(price.replace('$', '').replace('.', '').replace(',', '.'))

            # Verificar si ya hemos visto este producto
            if name not in product_names_seen:
                products_data.append({"Product Name": name, "Price": price, "Store": 'Jumbo'})
                product_names_seen.add(name)  # Añadir el nombre del producto al set

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