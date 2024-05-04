from fastapi import FastAPI,status,Request
import mysql.connector
from fastapi.responses import JSONResponse
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import Query
from queries import *


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
    
# Get Detail Product
@app.get("/product-detail/{sku}")
async def get_product_detail(sku: str):
    try:
        cursor.execute(GET_DETAIL_PRODUCT_QUERY, (sku,))
        products = cursor.fetchall()

        product_dicts = []
        for product in products:
            prices = product[8].split(';') if product[8] else []
            measure_units = product[9].split(';') if product[9] else []
            product_dict = {
                "sku": product[0],
                "webName": product[1],
                "image": product[2],
                "specification": product[3],
                "ingredients": product[4],
                "dosageForm": product[5],
                "brand": product[6],
                "slug": product[7],
                "price": prices,
                "currencySymbol": product[10],
                "measureUnitName": measure_units,
            }
            product_dicts.append(product_dict)

        return product_dicts
    except mysql.connector.Error as error:
        print("Error fetching products:", error)
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

#Get Categories
@app.get("/getCategories")
async def getCategories():
    try:
        cursor.execute("""SELECT * FROM Categories""")
        categories = cursor.fetchall()

        categories_dicts = []
        for cate in categories:
            cate_dict = {
                "id": cate[0],
                "name": cate[1],
                "parentName": cate[2],
                "slug": cate[3],
                "level": cate[5]
            }
            categories_dicts.append(cate_dict)

        return categories_dicts
    except mysql.connector.Error as error:
        print("Error fetching categories:", error)
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.post("/register")
async def register(request: Request):
    try:
        body = await request.body()
        if not body:
            return {"error": "No data received", "status": status.HTTP_400_BAD_REQUEST}

        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return {"error": "Username and password are required", "status": status.HTTP_400_BAD_REQUEST}
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result:
                return {"error": "User already exists", "status": status.HTTP_400_BAD_REQUEST}

        with db.cursor() as cursor:
            cursor.execute("INSERT INTO User (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            return {"message": "User registered successfully", "status": status.HTTP_201_CREATED}
    except ValueError as e:
        return {"error": str(e), "status": status.HTTP_400_BAD_REQUEST}
    except mysql.connector.Error as error:
        db.rollback()
        return {"error": str(error), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}

@app.post("/login")
async def login(request: Request):
    try:
        body = await request.body()
        if not body:
            return {"error": "No data received", "status": status.HTTP_400_BAD_REQUEST}

        data = await request.json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Username and password are required", "status": status.HTTP_400_BAD_REQUEST}

        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM User WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user:
                return {
                    "message": "Login successful",
                    "user": {
                        "id": user[0],
                        "username": user[1],
                        "email": user[3],
                        "phone": user[4],
                        "address": user[5]
                    },
                    "status": status.HTTP_200_OK
                }
            return {"error": "Invalid username or password", "status": status.HTTP_401_UNAUTHORIZED}
        
    except ValueError as e:
        return {"error": str(e), "status": status.HTTP_400_BAD_REQUEST}
    except mysql.connector.Error as error:
        return {"error": str(error), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}

@app.get("/usersInfo")
def getUserInfo(username: str):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            return {"id": user[0], "username": user[1], "password": user[2], "email": user[3], "phone": user[4], "address": user[5]}
        return {"error": "User not found"}


@app.get("/search")
async def search_product(s: str = Query(None)):
    try:
        if s:
            cursor.execute(
                SEARCH_PRODUCTS_QUERY,
                (f"%{s}%", f"%{s}%", f"%{s}%", f"%{s}%")
            )
        else:
            # Nếu không có tham số tìm kiếm, trả về tất cả sản phẩm
            cursor.execute(GET_ALL_PRODUCTS_QUERY)

        products = cursor.fetchall()
        
        # Chuyển đổi kết quả thành dạng từ điển
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