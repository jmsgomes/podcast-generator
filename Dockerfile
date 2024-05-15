FROM ubuntu:latest

ENV VIRTUAL_ENV='/opt/venv'

RUN apt-get update && apt-get install -y \
  python3-full \
  python3-venv \
  python3-pip \
  git

RUN python3 -m venv "${VIRTUAL_ENV}"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN pip3 install PyYAML

COPY feed.py /usr/bin/feed.py

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
