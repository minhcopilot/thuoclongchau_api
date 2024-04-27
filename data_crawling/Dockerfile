FROM python:3.9.16-slim-buster
RUN pip install fastapi uvicorn
COPY . ./crawling
CMD [ "uvicorn", "crawling.main:app", "--host", "0.0.0.0", "--port", "8081" ]