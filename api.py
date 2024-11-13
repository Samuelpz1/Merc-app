from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from fastapi.responses import JSONResponse

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify allowed origins like ['http://127.0.0.1']
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (including OPTIONS)
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model to receive query data
class QueryRequest(BaseModel):
    query: str

# MySQL database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your DB username
        password="Test01",  # Replace with your DB password
        database="mercapp"  # Replace with your DB name
    )

# Route to handle the search query
@app.post("/search/")
async def search(query_request: QueryRequest):
    query = query_request.query
    results = []

    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Perform a query to search for products that match the query
    """sql_query = 
        SELECT nom_product, precio, tienda 
        FROM resultados 
        WHERE nom_product LIKE %s
    """# Modify the cursor.execute line like this:
    cursor.execute("SELECT * FROM resultados WHERE nom_product LIKE %s ORDER BY precio ASC LIMIT 5", (f"%{query}%",))
    #cursor.execute(sql_query, ('%' + query + '%','ORDER BY precio ASC LIMIT 5 '))  # Using % for partial match

    # Fetch the results
    rows = cursor.fetchall()

    for row in rows:
        results.append({
            "nom_product": row["nom_product"],
            "precio": row["precio"],
            "tienda": row["tienda"]
        })

    cursor.close()
    connection.close()

    # Return the results as a JSON response
    return JSONResponse(content={"results": results})
