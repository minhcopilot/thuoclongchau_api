#Tạo môi trường ảo với các gói lib
python -m venv env

#Chạy môi trường ảo  
env\Scripts\activate

#tải các thư viện cho môi trường ảo
pip install -r requirements.txt

#chạy app
uvicorn main:app --reload
uvicorn app.main:app --reload


