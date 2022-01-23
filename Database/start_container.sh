#!/bin/bash

# Script de lancement du docker une fois
# l'image crée
# Fournir dans l'ordre, en argument
# 1 nom du containe
# 2 nom de l'image 
hostname=$1
dnssearch="projet.local"
dns1=192.168.1.3
dns2=1.1.1.1
image=$2

sudo docker run -d --hostname $hostname --cap-add=NET_ADMIN --log-driver syslog --log-opt syslog-address=tcp://192.168.1.3:1456 --dns-search $dnssearch --dns $dns1 --dns $dns2 --name $hostname $image
