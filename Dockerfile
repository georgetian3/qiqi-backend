FROM python:3.11.5

COPY requirements.txt ./
COPY setup.sh ./
RUN setup.sh

COPY . .

RUN run.sh