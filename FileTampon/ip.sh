#! /bin/sh

ip a flush eth0
ip a add 192.168.1.78/24 dev eth0
ip r add default via 192.168.1.222 dev eth0
python ./app.py


