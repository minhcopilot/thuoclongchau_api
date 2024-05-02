from fastapi import FastAPI,status
import mysql.connector
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
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
    insert_product_query = """
        INSERT INTO Products (sku, name, webName, image, slug, ingredients, dosageForm, brand, displayCode,
                              isActive, isPublish, searchScoring, productRanking, specification)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            webName = VALUES(webName),
            image = VALUES(image),
            slug = VALUES(slug),
            ingredients = VALUES(ingredients),
            dosageForm = VALUES(dosageForm),
            brand = VALUES(brand),
            displayCode = VALUES(displayCode),
            isActive = VALUES(isActive),
            isPublish = VALUES(isPublish),
            searchScoring = VALUES(searchScoring),
            productRanking = VALUES(productRanking),
            specification = VALUES(specification)
    """
    product_values = (
        product["sku"], product["name"], product["webName"], product["image"], product["slug"],
        product["ingredients"], product["dosageForm"], product["brand"], product["displayCode"],
        product["isActive"], product["isPublish"], product["searchScoring"], product["productRanking"],
        product["specification"]
    )
    cursor.execute(insert_product_query, product_values)

    for price in product["prices"]:
        save_price(product["sku"], price)

    for category in product["category"]:
        save_category(product["sku"], category)

def save_price(product_sku, price):
    insert_price_query = """
        INSERT INTO Prices (id, productSKU, measureUnitCode, measureUnitName, isSellDefault, price,
                            currencySymbol, isDefault, inventory, isInventory, level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            measureUnitCode = VALUES(measureUnitCode),
            measureUnitName = VALUES(measureUnitName),
            isSellDefault = VALUES(isSellDefault),
            price = VALUES(price),
            currencySymbol = VALUES(currencySymbol),
            isDefault = VALUES(isDefault),
            inventory = VALUES(inventory),
            isInventory = VALUES(isInventory),
            level = VALUES(level)
    """
    price_values = (
        price["id"], product_sku, price["measureUnitCode"], price["measureUnitName"],
        price["isSellDefault"], price["price"], price["currencySymbol"], price["isDefault"],
        price["inventory"], price["isInventory"], price["level"]
    )
    cursor.execute(insert_price_query, price_values)

def save_category(product_sku, category):
    insert_category_query = """
        INSERT INTO Categories (id, name, parentName, slug, level, isActive, productSKU)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            parentName = VALUES(parentName),
            slug = VALUES(slug),
            level = VALUES(level),
            isActive = VALUES(isActive)
    """
    category_values = (
        category["id"], category["name"], category["parentName"], category["slug"], category["level"],
        category["isActive"], product_sku
    )
    cursor.execute(insert_category_query, category_values)

@app.post("/save_products")
def save_products():
    API_URL = "http://localhost:8081/crawl_products" 
    
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        products = data.get("products", [])

        try:
            for product in products:
                save_product(product)
            db.commit()
            return {"message": "Data saved successfully"}
        except mysql.connector.Error as error:
            db.rollback()  
            return {"error": str(error)}, status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        print(f"Lỗi khi gọi API: {response.status_code} - {response.text}")
        return []