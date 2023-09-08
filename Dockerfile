FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip

COPY requirements.txt /requirements.txt


RUN apk update && \
    apk add mysql-client mysql-dev libjpeg-turbo-dev mariadb-dev gcc

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers musl-dev zlib zlib-dev 
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
RUN apk add postgresql-dev
RUN apk add --no-cache postgresql-dev gcc musl-dev
RUN pip install psycopg2

RUN cp /usr/share/zoneinfo/America/Bogota /etc/localtime

RUN mkdir /code
WORKDIR /code
COPY . /code/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]