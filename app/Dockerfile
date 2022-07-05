FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app /static /media
WORKDIR /app

RUN apt-get update && apt-get install -y python3-dev python3-pip musl-dev build-essential libpq-dev

RUN pip install --upgrade pip
RUN pip install setuptools wheel
COPY ./requirements.txt .
RUN pip install --no-cache-dir --default-timeout=500 -r requirements.txt

CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1 ; done && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py createsuperuser_if_none_exists --user=${SUPERUSER} --password=${PASSWORD} --email=${EMAIL}; \
    gunicorn -w 5 -b 0.0.0.0:8000 core.asgi:application -k uvicorn.workers.UvicornWorker