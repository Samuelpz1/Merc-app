
import pandas as pd
import mysql.connector

if __name__ == "__main__":
    #Store , link , cards , price , name , search bar , search button 
    info = {
        'Jumbo': ('https://www.tiendasjumbo.co/supermercado/despensa' , '.tiendasjumboqaio-cmedia-integration-cencosud-0-x-galleryItem' , 'div.tiendasjumboqaio-jumbo-minicart-2-x-price','span.vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName','.vtex-styleguide-9-x-input','.vtex-store-components-3-x-searchBarIcon'),
        'Exito': ('https://www.exito.com/mercado/despensa', 'article.productCard_productCard__M0677','.ProductPrice_container__price__XmMWA','.styles_name__qQJiK','[data-testid="store-input"]','[data-testid="store-button"]'),
        'D1': ('https://domicilios.tiendasd1.com/ca/alimentos-y-despensa/ALIMENTOS%20Y%20DESPENSA', 'div.styles__StyledCard-sc-3jvmda-0','p.CardBasePrice__CardBasePriceStyles-sc-1dlx87w-0','p.CardName__CardNameStyles-sc-147zxke-0','[placeholder="Buscar en Bogota Tienda Domicilios"]','[data-testid="search-action-icon"]'),
        'Vaquita': ('https://lavaquita.co/collections/despensa','.productitem','.productitem .price--main .money', '.productitem .productitem--title','.form-field-input.live-search-form-field','.live-search-button')
        
    }
    db_connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Test01',
        database = 'mercapp')
    cursor = db_connection.cursor()
    # Obtener valores de canasta_basica
    query = "SELECT prod_id, prod_category FROM canasta_basica"
    cursor.execute(query)

    # Crear un diccionario usando los valores obtenidos
    canasta_basica = {prod_id: prod_category for prod_id, prod_category in cursor.fetchall()}
    '''canasta_basica = {
        1 : 'Leche',
        2 : 'Huevos'
    }'''
    # Cerramos la conexión
    cursor.close()
    db_connection.close()
    test = {
        'D1': ('https://domicilios.tiendasd1.com/ca/alimentos-y-despensa/ALIMENTOS%20Y%20DESPENSA', 'div.styles__StyledCard-sc-3jvmda-0','p.CardBasePrice__CardBasePriceStyles-sc-1dlx87w-0','p.CardName__CardNameStyles-sc-147zxke-0','[placeholder="Buscar en Bogota Tienda Domicilios"]','[data-testid="search-action-icon"]'),
    }

    from research import research 
    research(canasta_basica,info)
