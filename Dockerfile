FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    pkg-config \
    default-libmysqlclient-dev \
    nginx \
    curl \
    git

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "web_flask.app:app"]
