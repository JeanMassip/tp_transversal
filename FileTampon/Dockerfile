FROM python:3.8-alpine

COPY main.py .
COPY requirements.txt .
RUN apk update && apk upgrade
RUN apk add openssh-server openssh-client syslog-ng bind-tools
COPY entrypoint.sh .
COPY filetamponsyslog-ng.conf /etc/syslog-ng/

RUN pip install -r requirements.txt

ENTRYPOINT ["./ip.sh"]
