from datetime import date
import mysql.connector

def insert (df,category):
    db_connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Test01',
        database = 'mercapp'

    )

    cursor = db_connection.cursor()
    for index, row in df.iterrows():
        sql = 'INSERT INTO resultados (nom_product, precio, tienda, prod_category_id, fecha) VALUES (%s, %s, %s, %s, %s)'
        values = (row['Product Name'], row['Price'], row['Store'], category, date.today())
        cursor.execute(sql, values)
    db_connection.commit()
    cursor.close()
    db_connection.close()
