import requests
import json
from dotenv import load_dotenv
import mysql.connector
import os
from pathlib import Path
from fastapi import FastAPI, status
from apscheduler.schedulers.background import BackgroundScheduler

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
API_URL = "https://api.nhathuoclongchau.com.vn/lccus/search-product-service/api/products/ecom/product/search/cate"
MAX_RESULT_COUNT = 5
try:
    cursor = db.cursor()
    sql = "SELECT current_skip_count FROM SkipCount ORDER BY current_skip_count DESC LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        current_skip_count = result[0]
    else:
        current_skip_count = 0
except mysql.connector.Error as error:
    print(f"Error retrieving current_skip_count: {error}")
    current_skip_count = 0


def crawl_data():
    global current_skip_count
    body = {"skipCount": current_skip_count, "maxResultCount": MAX_RESULT_COUNT}
    response = requests.post(API_URL, json=body)
    if response.status_code == 200:
        data = response.json()
        save_response = requests.post("http://api_service:8080/save_products", data=json.dumps(data))
        if save_response.status_code == 200:
            current_skip_count += MAX_RESULT_COUNT
            print(f"{MAX_RESULT_COUNT} sản phẩm đã được lưu thành công")
            try:
                cursor = db.cursor()
                sql = "INSERT INTO SkipCount (current_skip_count) VALUES (%s) ON DUPLICATE KEY UPDATE current_skip_count = %s"
                cursor.execute(sql, (current_skip_count, current_skip_count))
                db.commit()
            except mysql.connector.Error as error:
                print(f"Error saving current_skip_count: {error}")
                db.rollback()
        else:
            print(f"Lỗi lưu dữ liệu: {save_response.text}")
        return data["products"], MAX_RESULT_COUNT
    return None, None

@app.get("/crawl_products")
def crawl_products():
    products, max_result_count = crawl_data()
    if products is None:
        return {"error": "Không thể lấy dữ liệu"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"message": f"{max_result_count} sản phẩm đã được lưu thành công"}

scheduler = BackgroundScheduler()
scheduler.add_job(crawl_products, 'interval', seconds=10)
scheduler.start()

