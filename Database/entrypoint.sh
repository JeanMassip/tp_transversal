#! /bin/sh
# Configuration de l'interface réseau
ip a flush eth0
ip a add 192.168.1.8/24 dev eth0
ip r add default via 192.168.1.1 dev eth0
# Lancement de l'application et service actif du container
# python ./app.py
tail -f /dev/null
