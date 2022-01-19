FROM python:3.8-alpine

ADD main.py .
ADD requirements.txt .
ADD ip.sh .
RUN apk update && apk upgrade
RUN apk add openssh-server openssh-client syslog-ng bind-tools

RUN pip install -r requirements.txt

ENTRYPOINT ["./ip.sh"]
