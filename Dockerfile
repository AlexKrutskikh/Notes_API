FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/


RUN openssl req -x509 -newkey rsa:4096 -keyout /app/cert.key -out /app/cert.crt -days 365 -nodes \
    -subj "/CN=localhost"

CMD ["python", "manage.py", "runserver_plus", "--cert-file", "cert.crt", "--key-file", "cert.key", "0.0.0.0:8000"]
