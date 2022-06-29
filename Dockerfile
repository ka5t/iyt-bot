FROM python:3.9-alpine

RUN mkdir /opt/bot
COPY requirements.txt /opt/
WORKDIR /opt/bot
RUN pip3 install -r ../requirements.txt

COPY . .

ARG BOT_TOKEN

ENV BOT_TOKEN=$BOT_TOKEN
ENV BOT_STORAGE_LOCATION=/opt/botdb/db.pickle

CMD python3 src/run_bot.py
