FROM python:3.10

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt 

COPY . /app 

EXPOSE 9997

ENTRYPOINT ["python3", "server.py"]