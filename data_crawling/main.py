import requests
import json
from fastapi import FastAPI, status
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

app = FastAPI()
API_URL = "https://api.nhathuoclongchau.com.vn/lccus/search-product-service/api/products/ecom/product/search/cate"
MAX_RESULT_COUNT = 5
current_skip_count = 0

def crawl_data():
    global current_skip_count
    body = {"skipCount": current_skip_count, "maxResultCount": MAX_RESULT_COUNT}
    response = requests.post(API_URL, json=body)
    if response.status_code == 200:
        data = response.json()
        save_response = requests.post("http://localhost:8000/save_products", data=json.dumps(data))
        if save_response.status_code == 200:
            current_skip_count += MAX_RESULT_COUNT
            print(f"{current_skip_count} sản phẩm đã được lưu thành công")
        else:
            print(f"Lỗi lưu dữ liệu: {save_response.text}")
        return data["products"], current_skip_count
    return None, None

@app.get("/crawl_products")
def crawl_products():
    products, skip_count = crawl_data()
    if products is None:
        return {"error": "Không thể lấy dữ liệu"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"message": f"{skip_count} sản phẩm đã được lưu thành công"}

scheduler = BackgroundScheduler()
scheduler.add_job(crawl_products, 'interval', seconds=10)
scheduler.start()

