FROM python:3.8.6-buster

COPY requirements.txt /home/requirements.txt

WORKDIR /home

RUN pip install -U pip
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com
RUN python3 -m pip install --no-cache -r requirements.txt

EXPOSE 8000

CMD [ "python3", "/home/lipotes-b/manage.py", "runserver", "0.0.0.0:8000" ]