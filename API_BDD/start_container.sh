#!/bin/bash

# Script de lancement du docker une fois
# l'image crée 
hostname=$1
dnssearch="projet.local"
dns1=192.168.1.3
dns2=1.1.1.1
image="bddtest"

sudo docker run -d --hostname $hostname --cap-add=NET_ADMIN --log-driver syslog --log-opt syslog-address=tcp://192.168.1.3:1454 --dns-search $dnssearch --dns $dns1 --dns $dns2 --name $hostname $image
