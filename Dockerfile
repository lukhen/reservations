FROM python:3.10.2-alpine

COPY ./requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app

RUN apk update && \
    apk add netcat-openbsd

RUN apk add --no-cache mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps \
        build-base \
        mariadb-dev ;\
    pip install mysqlclient;\
    apk del .build-deps

RUN apk add --no-cache postgresql-dev; \
    apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    && pip install psycopg2 \
    && apk del --no-cache .build-deps

RUN pip install -r requirements.txt
    
COPY . /usr/src/app

ENV FLASK_APP=project/__init__.py
ENV FLASK_ENV=development

CMD ["sh", "-c", "sleep 10 && gunicorn -b 0.0.0.0:5000 wsgi:app"]