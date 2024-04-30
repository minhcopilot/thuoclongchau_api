Đối với service data_crawling thì là như sau để chạy được:
Trỏ vào thư mục như sau:
(python_course) D:\DaiHoc\HK223_2023_2024\ChuyenDeNNLT\python_course_223\ThuocLongChau_API_Project\data_crawling>

#Tạo môi trường ảo với các gói lib
python -m venv env

#Chạy môi trường ảo  
env\Scripts\activate

#tải các thư viện cho môi trường ảo
pip install -r requirements.txt

#chạy app
uvicorn main:app --reload


Đối với service mysql_api thì là như sau để chạy được:
Trỏ vào thư mục như sau:
(python_course) D:\DaiHoc\HK223_2023_2024\ChuyenDeNNLT\python_course_223\ThuocLongChau_API_Project\mysql_api>

#Tạo môi trường ảo với các gói lib
python -m venv env

#Chạy môi trường ảo  
env\Scripts\activate

#tải các thư viện cho môi trường ảo
pip install -r requirements.txt

#chạy app
uvicorn app.main:app --reload


