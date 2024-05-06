import requests
import json
from dotenv import load_dotenv
import mysql.connector
import os
from pathlib import Path
from fastapi import FastAPI, status, Request
from apscheduler.schedulers.background import BackgroundScheduler
from logger import logger

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Environment variables
DATABASE_NAME = os.getenv("DB_NAME")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

db = mysql.connector.connect(
    host=HOST, user=USER, password=PASSWORD, database=DATABASE_NAME, port=PORT
)

app = FastAPI()

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    log_dict = {
        "method": request.method,
        "url": request.url,
    }
    logger.info(log_dict)
    response = await call_next(request)
    return response

API_URL = "https://api.nhathuoclongchau.com.vn/lccus/search-product-service/api/products/ecom/product/search/cate"
MAX_RESULT_COUNT = 5

def get_current_skip_count(cursor):
    try:
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
    return current_skip_count

def crawl_data(current_skip_count):
    logger.info('Bắt đầu crawl dữ liệu từ web')
    body = {"skipCount": current_skip_count, "maxResultCount": MAX_RESULT_COUNT}
    response = requests.post(API_URL, json=body)
    if response.status_code == 200:
        data = response.json()
        save_response = requests.post("http://api_service:8080/save_products", data=json.dumps(data))
        if save_response.status_code == 200:
            current_skip_count += MAX_RESULT_COUNT
            logger.info(f"{MAX_RESULT_COUNT} sản phẩm đã được lưu thành công")
            print(f"{MAX_RESULT_COUNT} sản phẩm đã được lưu thành công")
            return data["products"], MAX_RESULT_COUNT
        else:
            logger.error('Lỗi khi crawl dữ liệu')
            print(f"Lỗi lưu dữ liệu: {save_response.text}")
    return None, None

def save_current_skip_count(db, current_skip_count):
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO SkipCount (current_skip_count) VALUES (%s) ON DUPLICATE KEY UPDATE current_skip_count = %s"
            cursor.execute(sql, (current_skip_count, current_skip_count))
        db.commit()
    except mysql.connector.Error as error:
        print(f"Error saving current_skip_count: {error}")
        db.rollback()

@app.get("/crawl_products")
def crawl_products():
    with db.cursor() as cursor:
        current_skip_count = get_current_skip_count(cursor)
    products, max_result_count = crawl_data(current_skip_count)
    if products is None:
        return {"error": "Không thể lấy dữ liệu"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    save_current_skip_count(db, current_skip_count+ max_result_count)
    return {"message": f"{max_result_count} sản phẩm đã được lưu thành công"}

scheduler = BackgroundScheduler()
# scheduler.add_job(save_products, 'cron', hour=0, minute=0)  # Chạy vào lúc 00:00
scheduler.add_job(crawl_products, 'interval', seconds=20, max_instances=1)
scheduler.start()