FROM mysql

ENV MYSQL_ROOT_PASSWORD psw123
ADD ./init_db/init.sql /docker-entrypoint-initdb.d/init.sql
EXPOSE 3306
