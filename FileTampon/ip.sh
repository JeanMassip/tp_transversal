#! /bin/sh

ip a flush eth0
ip a add 192.168.1.78/24 dev eth0
ip r add default via 192.168.1.222 dev eth0
echo 'search projet.local' > /etc/resolv.conf
echo 'domain projet.local' >> /etc/resolv.conf
echo 'nameserver 192.168.1.3' >> /etc/resolv.conf
echo 'nameserver 1.1.1.1' >> /etc/resolv.conf
python ./app.py


