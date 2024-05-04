import logging
import sys

# Tạo logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Định dạng log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Ghi log vào file với encoding utf-8
file_handler = logging.FileHandler('data_crawling.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Ghi log ra console với encoding utf-8
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)