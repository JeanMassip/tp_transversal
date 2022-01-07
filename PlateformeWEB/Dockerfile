FROM python:latest

#Commands required to connect container to network
RUN ip a flush eth0
#Replace with specfic IP
RUN ip a add 192.168.1.12
RUN ip r add 192.168.1.0/24 dev eth0
RUN ip r add default via 192.168.1.1 dev eth0

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]