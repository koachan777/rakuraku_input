FROM python:3.11.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN apt-get update && apt-get install -y default-mysql-client

RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code