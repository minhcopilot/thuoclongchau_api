import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from fastapi import FastAPI
import requests

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Environment variables
DATABASE_NAME = os.getenv("DB_NAME")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

# Database connection
db = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE_NAME,
    port=PORT
)
cursor = db.cursor()

app = FastAPI()

# Global variables
current_skip_count = 0
API_URL = "https://api.nhathuoclongchau.com.vn/lccus/search-product-service/api/products/ecom/product/search/cate"
MAX_RESULT_COUNT = 5

# Helper functions
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

@app.get("/")
def index():
    return {"title": "Hello :)"}

@app.get("/save_products")
def save_products():
    global current_skip_count
    body = {"skipCount": current_skip_count, "maxResultCount": MAX_RESULT_COUNT}
    response = requests.post(API_URL, json=body)

    if response.status_code == 200:
        data = response.json()

        for product in data["products"]:
            save_product(product)

        db.commit()
        current_skip_count += MAX_RESULT_COUNT
        return {"message": "Data saved successfully"}

    else:
        return {"error": f"Request failed with status code: {response.status_code}"}

# Cấu hình lịch trình để crawl dữ liệu hằng ngày 
# scheduler = BackgroundScheduler()
# scheduler.add_job(save_products, 'cron', hour=0, minute=0)  # Run at 00:00
# scheduler.add_job(save_products, 'interval', seconds=10)  # Chạy sau 10 giây sử dụng seconds, minutes, hours hoặc days.
# scheduler.start()

# Stop background tasks on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    # scheduler.shutdown()
    db.close()