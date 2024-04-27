from fastapi import FastAPI
import requests
import mysql.connector

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_NAME=os.getenv("DB_NAME")
HOST=os.getenv("DB_HOST")
PORT=os.getenv("DB_PORT")
USER=os.getenv("DB_USER")
PASSWORD=os.getenv("DB_PASSWORD")
# Kết nối đến cơ sở dữ liệu MySQL
db = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE_NAME,
    port=PORT
)
cursor = db.cursor()

app = FastAPI()

current_skip_count = 0

@app.get("/")
def index():
    return {"title": "Hello:)"}
@app.get("/save_products")
async def save_products():
    global current_skip_count
    max_result_count = 5
    url = "https://api.nhathuoclongchau.com.vn/lccus/search-product-service/api/products/ecom/product/search/cate"
    body = {"skipCount": current_skip_count, "maxResultCount": max_result_count}
    response = requests.post(url, json=body)

    # Kiểm tra nếu yêu cầu thành công
    if response.status_code == 200:
        data = response.json()

        # Xử lý dữ liệu và lưu vào cơ sở dữ liệu
        for product in data["products"]:
            # Lưu thông tin sản phẩm vào bảng products
            insert_product_query = """
                INSERT INTO products (sku, name, webName, image, slug, ingredients, dosageForm, brand, displayCode, isActive, isPublish, searchScoring, productRanking, specification)
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
                product["sku"], product["name"], product["webName"], product["image"], product["slug"], product["ingredients"],
                product["dosageForm"], product["brand"], product["displayCode"], product["isActive"], product["isPublish"],
                product["searchScoring"], product["productRanking"], product["specification"]
            )
            cursor.execute(insert_product_query, product_values)

            # Lưu thông tin giá của sản phẩm vào bảng prices
            for price in product["prices"]:
                insert_price_query = """
                    INSERT INTO prices (id,productSKU, measureUnitCode, measureUnitName, isSellDefault, price, currencySymbol, isDefault, inventory, isInventory, level)
                    VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                    price["id"],product["sku"], price["measureUnitCode"], price["measureUnitName"], price["isSellDefault"], price["price"],
                    price["currencySymbol"], price["isDefault"], price["inventory"], price["isInventory"], price["level"]
                )
                cursor.execute(insert_price_query, price_values)
            
            # Lưu thông tin danh mục của sản phẩm vào bảng categories
            for category in product["category"]:
                insert_category_query = """
                INSERT INTO categories (id, name, parentName, slug, level, isActive, productSKU)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name), parentName=VALUES(parentName), slug=VALUES(slug), level=VALUES(level), isActive=VALUES(isActive);
                """
                category_values = (
                    category["id"], category["name"], category["parentName"], category["slug"], category["level"],
                    category["isActive"], product["sku"]
                )
                cursor.execute(insert_category_query, category_values)

        # Commit các thay đổi vào cơ sở dữ liệu
        db.commit()
        current_skip_count += max_result_count
        return {"message": "Dữ liệu đã được lưu thành công vào cơ sở dữ liệu"}

    # Trả về thông báo lỗi nếu yêu cầu không thành công
    else:
        return {"error": f"Yêu cầu không thành công. Mã lỗi: {response.status_code}"}