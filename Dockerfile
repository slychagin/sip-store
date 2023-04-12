FROM python:3.10-alpine3.17
LABEL maintainer='sil.patelnya@gmail.com'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY . .

WORKDIR /sip
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home sip && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R sip:sip /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER sip
