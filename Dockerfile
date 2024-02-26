FROM ubuntu:22.04
WORKDIR /app
RUN apt-get update \
    && apt-get install -y \
    python3.9 \
    python3-dev \
    python3-pip \
    python3-pil \
    python3-numpy \
    gcc
COPY requirements.txt .
RUN pip3 install -r requirements.txt