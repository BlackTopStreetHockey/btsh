FROM python:3.13.0-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip install -U pip setuptools wheel && pip install -r requirements.txt
