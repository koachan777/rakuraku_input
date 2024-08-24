FROM python:3.11.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN apt-get update && apt-get install -y default-mysql-client

RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/

RUN echo 'alias pmrun="python3 manage.py runserver 0.0.0.0:8000"' >> ~/.bashrc
RUN echo 'alias pmdb="python3 manage.py dbshell"' >> ~/.bashrc
RUN echo 'alias pm="python3 manage.py"' >> ~/.bashrc