from fastapi import FastAPI,status,Request
import mysql.connector
from fastapi.responses import JSONResponse
import os
from pathlib import Path
from dotenv import load_dotenv
from queries import INSERT_PRODUCT_QUERY, INSERT_PRICE_QUERY, INSERT_CATEGORY_QUERY, GET_ALL_PRODUCTS_QUERY

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Environment variables
DATABASE_NAME = os.getenv("DB_NAME")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

db = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE_NAME,
    port=PORT
)
cursor = db.cursor()

app = FastAPI()

def save_product(product):
    product_values = (
        product["sku"], product["name"], product["webName"], product["image"], product["slug"],
        product["ingredients"], product["dosageForm"], product["brand"], product["displayCode"],
        product["isActive"], product["isPublish"], product["searchScoring"], product["productRanking"],
        product["specification"]
    )
    cursor.execute(INSERT_PRODUCT_QUERY, product_values)

    for price in product["prices"]:
        save_price(product["sku"], price)

    for category in product["category"]:
        save_category(product["sku"], category)

def save_price(product_sku, price):
    price_values = (
        price["id"], product_sku, price["measureUnitCode"], price["measureUnitName"],
        price["isSellDefault"], price["price"], price["currencySymbol"], price["isDefault"],
        price["inventory"], price["isInventory"], price["level"]
    )
    cursor.execute(INSERT_PRICE_QUERY, price_values)

def save_category(product_sku, category):
    category_values = (
        category["id"], category["name"], category["parentName"], category["slug"], category["level"],
        category["isActive"], product_sku
    )
    cursor.execute(INSERT_CATEGORY_QUERY, category_values)

@app.post("/save_products")
async def save_products(request: Request):
    try:
        body = await request.body()
        if not body:
            return {"error": "No data received"}, status.HTTP_400_BAD_REQUEST

        data = await request.json()
        products = data.get("products", [])

        if not products:
            return {"error": "No products found in the data"}, status.HTTP_400_BAD_REQUEST

        for product in products:
            save_product(product)
        db.commit()
        return {"message": "Data saved successfully"}
    except ValueError as e:
        return {"error": str(e)}, status.HTTP_400_BAD_REQUEST
    except mysql.connector.Error as error:
        db.rollback()
        return {"error": str(error)}, status.HTTP_500_INTERNAL_SERVER_ERROR
    
#Get All Product
@app.get("/products")
async def get_products():
    try:
        cursor.execute(GET_ALL_PRODUCTS_QUERY)
        products = cursor.fetchall()

        product_dicts = []
        for product in products:
            prices = product[4].split(';') if product[4] else []
            measure_units = product[6].split(';') if product[6] else []
            product_dict = {
                "sku": product[0],
                "webName": product[1],
                "image": product[2],
                "specification": product[3],
                "price": prices,
                "currencySymbol": product[5],
                "measureUnitName": measure_units,
            }
            product_dicts.append(product_dict)

        return product_dicts
    except mysql.connector.Error as error:
        print("Error fetching products:", error)
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})