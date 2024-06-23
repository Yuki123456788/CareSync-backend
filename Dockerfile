FROM python:3.12-slim-bookworm

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config

WORKDIR /app
COPY . .

RUN python3 -m pip install -U pip
RUN python3 -m pip install -U setuptools
RUN pip install poetry==1.8.2
RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-interaction --no-ansi

ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]
