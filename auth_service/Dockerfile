FROM python:3.10-slim

RUN apt-get update && apt-get install -y netcat

RUN mkdir /auth
WORKDIR /auth

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

RUN pip3 install --upgrade pip &&  \
    pip3 install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
