import requests
from fastapi import FastAPI, status
from apscheduler.schedulers.background import BackgroundScheduler
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
        current_skip_count += MAX_RESULT_COUNT
        return data["products"], current_skip_count + MAX_RESULT_COUNT
    else:
        return None, None

@app.get("/crawl_products")
async def crawl_products():
    products, skip_count = crawl_data()
    if products is None:
        return {"error": "Failed to crawl data"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"products": products, "skip_count": skip_count}

