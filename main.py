from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

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
    

    #Getting prices

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(20)
    cards = driver.find_elements(By.CSS_SELECTOR, "div.tiendasjumboqaio-cmedia-integration-cencosud-0-x-galleryItem")
    
    for card in cards:
        name_element = card.find_element(By.CSS_SELECTOR, "span.vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName")
        price_element = card.find_element(By.CSS_SELECTOR, "div.tiendasjumboqaio-jumbo-minicart-2-x-price")
        price = price_element.text
        name = name_element.text
        products_data.append({"Product Name":name,"Price":price})
    time.sleep(10)
    driver.quit()

    df = pd.DataFrame(products_data)
    print(df)
 



if __name__ == "__main__":
    main()