FROM python:3.9.16-slim-buster

WORKDIR /data_crawling

COPY ./requirements.txt /data_crawling/requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        build-essential \
        && rm -rf /var/lib/apt/lists/*
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql" \
    MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]