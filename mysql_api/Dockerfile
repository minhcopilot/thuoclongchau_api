FROM python:3.9.16-slim-buster
RUN pip3 install fastapi uvicorn
COPY . ./api
CMD [ "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000" ]