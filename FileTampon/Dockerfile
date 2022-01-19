FROM python:3.8-alpine

ADD main.py .
ADD requirements.txt .
ADD ip.sh .

RUN pip install -r requirements.txt

ENTRYPOINT ["./ip.sh"]