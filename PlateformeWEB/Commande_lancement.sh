#!/bin/bash

# Script de lancement du docker une fois
# l'image crée 

hostname="......"
dnssearch="projet.local"
dns1=192.168.1.3
dns2=1.1.1.1
image="python:3.8-alpine"

sudo docker run -d --hostname $hostname --cap-add=NET_ADMIN --dns-search $dnssearch --dns $dns1 --dns $dns2 --name $hostname $image
