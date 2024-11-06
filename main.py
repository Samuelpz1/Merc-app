from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import mysql.connector

def main():
    #Store , link , cards , price , name , search bar , search button 
    info = {
        'Jumbo': ('https://www.tiendasjumbo.co/supermercado/despensa' , '.tiendasjumboqaio-cmedia-integration-cencosud-0-x-galleryItem' , 'div.tiendasjumboqaio-jumbo-minicart-2-x-price','span.vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName','.vtex-styleguide-9-x-input','.vtex-store-components-3-x-searchBarIcon'),
        'Exito': ('https://www.exito.com/mercado/despensa', 'article.productCard_productCard__M0677','.ProductPrice_container__price__XmMWA','.styles_name__qQJiK','[data-testid="store-input"]','[data-testid="store-button"]'),
        'D1': ('https://domicilios.tiendasd1.com/ca/alimentos-y-despensa/ALIMENTOS%20Y%20DESPENSA', 'div.styles__StyledCard-sc-3jvmda-0','p.CardBasePrice__CardBasePriceStyles-sc-1dlx87w-0','p.CardName__CardNameStyles-sc-147zxke-0','[placeholder="Buscar en Bogota Tienda Domicilios"]','[data-testid="search-action-icon"]'),
        'Vaquita': ('https://lavaquita.co/collections/despensa','.productitem','.productitem .price--main .money', '.productitem .productitem--title','.form-field-input.live-search-form-field','.live-search-button')
        
    }
    input_u = input('Introduce el nombre del producto que deseas buscar: ')
    output = []
    for store in info:
        store_data = research(store ,info[store][0], info[store][1],info[store][2], info[store][3], info[store][4], info[store][5],input_u)
        output.append(store_data)
    #print(research('D1' ,info['D1'][0], info['D1'][1],info['D1'][2], info['D1'][3], info['D1'][4], info['D1'][5],input_u))

    final_df = pd.concat(output, ignore_index=True)
    print(f"Estos son los resultados para tu búsqueda en los principales supermercados:\n")
    print(final_df)

def research (store , link , cards , price , name, search_bar ,search_button, input_u):
    
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")

    #Open the website
    option.add_argument("--window-size=1920,1800")
    driver = Chrome(service=service,options=option)
    driver.get(link)
    time.sleep(2)

    #Creting empty df
    products_data = []
    product_names_seen = set()  # Set to keep track of unique product names

    #Search the product
    driver.find_element(By.CSS_SELECTOR,search_bar).send_keys(input_u)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,search_button).click()
    time.sleep(2)



    #Getting prices

    last_height = driver.execute_script("return document.body.scrollHeight")
    products_collected = 0  # Variable para contar los productos recopilados
    max_products = 3  # Número máximo de productos a recopilar
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
            #Print(name_element,price_element)


            # Verificar si ya hemos visto este producto
            if name_element not in product_names_seen:
                products_data.append({"Product Name": name_element, "Price": price_element, "Store": store})
                product_names_seen.add(name_element)  # Añadir el nombre del producto al set
                products_collected += 1  # Incrementar el contador de productos

            # Si ya se han recolectado los tres productos, salir del bucle
            if products_collected >= max_products:
                break
        # Si hemos recolectado los tres productos, salimos del bucle
        if products_collected >= max_products:
            break

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
    
    return df 
'''
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
    db_connection.close()'''

if __name__ == "__main__":
    main()