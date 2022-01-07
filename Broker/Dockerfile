FROM python:latest

ADD handler.py .
ADD main.py .
ADD receiver.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

#Commands required to connect container to network
RUN ip a flush eth0
#Replace with specfic IP
RUN ip a add 192.168.1.8
RUN ip r add 192.168.1.0/24 dev eth0
RUN ip r add default via 192.168.1.1 dev eth0

ENTRYPOINT [ "python", "./app.py" ]